import customtkinter as ctk
import random
import string
import threading
import time
import requests
import os
import re

class PortableChat:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Portable Chat")
        self.root.geometry("380x350")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.92)
        self.root.configure(fg_color="#1a1a1a")

        self.api_key = ""
        self.username = ""
        self.room_code = ""
        self.last_msg_id = None 
        self.session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.running = True
        
        self.user_colors = {}
        self.colors = ["#ff5555", "#50fa7b", "#8be9fd", "#ff79c6", "#bd93f9", "#ffb86c", "#f1fa8c"]
        self.online_users = {}

        self.triggers = [";", "/"]
        self.blacklisted = ["cp", "gore", "slur", "nazi", "hitler"]

        self.display = ctk.CTkTextbox(
            self.root,
            width=360,
            height=220,
            state="disabled",
            fg_color="#121212",
            text_color="#e0e0e0",
            font=("Consolas", 12)
        )
        self.display.pack(pady=10, padx=10)
        
        for i, color in enumerate(self.colors):
            self.display.tag_config(f"color{i}", foreground=color)
        self.display.tag_config("system", foreground="#888888")

        self.input = ctk.CTkEntry(
            self.root,
            placeholder_text="Press ; or / to type...",
            width=360
        )
        self.input.pack(pady=5, padx=10)
        self.input.bind("<Return>", self.send)
        self.input.configure(state="disabled")

        self.status = ctk.CTkLabel(
            self.root,
            text="F1: HOST | F2: JOIN | F3: WHO | ESC: UNLOCK",
            text_color="gray"
        )
        self.status.pack()

        for k in self.triggers:
            self.root.bind(f"<KeyPress-{k}>", self.focus_chat)
        self.root.bind("<F1>", lambda e: self.host())
        self.root.bind("<F2>", lambda e: self.join())
        self.root.bind("<F3>", lambda e: self.send_system("WHO"))
        self.root.bind("<Escape>", self.unfocus_chat)
        self.root.bind("<ButtonPress-1>", self.move_start)
        self.root.bind("<B1-Motion>", self.move_drag)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.init_app()
        self.root.mainloop()

    def get_user_color_tag(self, user):
        if user not in self.user_colors:
            self.user_colors[user] = f"color{len(self.user_colors) % len(self.colors)}"
        return self.user_colors[user]

    def write(self, user, msg, is_system=False):
        self.display.configure(state="normal")
        if is_system:
            self.display.insert("end", f"{msg}\n", "system")
        else:
            tag = self.get_user_color_tag(user)
            self.display.insert("end", f"{user}: ", tag)
            self.display.insert("end", f"{msg}\n")
        self.display.see("end")
        self.display.configure(state="disabled")

    def apply_filter(self, text):
        t = text.lower().replace(" ", "")
        if re.search(r"(http|https|www|\.com|\.net|\.org|://)", t):
            return "################ (LINK BLOCKED)"
        for word in self.blacklisted:
            if word in t:
                return "******** (INAPPROPRIATE)"
        return text

    def listen(self):
        url = f"https://rest.ably.io/channels/{self.room_code}/history"
        auth = tuple(self.api_key.split(":"))

        try:
            r = requests.get(url, params={"limit": 1}, auth=auth, timeout=5)
            if r.status_code == 200 and r.json():
                self.last_msg_id = r.json()[0]["id"]
        except: pass

        while self.running:
            try:
                r = requests.get(url, params={"limit": 1}, auth=auth, timeout=5)
                if r.status_code == 200:
                    history = r.json()
                    if history:
                        msg_obj = history[0]
                        new_id = msg_obj["id"]

                        if new_id != self.last_msg_id:
                            self.last_msg_id = new_id 
                            raw_data = msg_obj["data"]

                            if raw_data.startswith("SYSTEM:"):
                                parts = raw_data.split(":", 4)
                                if len(parts) >= 4:
                                    _, kind, user, sid, extra = parts
                                    if kind == "JOIN":
                                        self.online_users[user] = sid
                                        if sid != self.session_id:
                                            self.write(None, f"[+] {user} joined", True)
                                    elif kind == "LEAVE":
                                        self.online_users.pop(user, None)
                                        self.write(None, f"[-] {user} left", True)
                                    elif kind == "WHO" and self.session_id == sid:
                                        users = ", ".join(self.online_users.keys())
                                        self.send_system("LIST", users)
                                    elif kind == "LIST":
                                        self.write(None, f"[Online] {extra}", True)
                            else:
                                parts = raw_data.split(":", 2)
                                if len(parts) == 3:
                                    user, sid, text = parts
                                    if sid != self.session_id:
                                        self.write(user, text)
            except:
                pass
            time.sleep(0.6)

    def send(self, e=None):
        raw = self.input.get().strip()
        if not raw or not self.room_code: return

        msg = self.apply_filter(raw)
        payload = f"{self.username}:{self.session_id}:{msg}"

        self.write(self.username, msg) 

        url = f"https://rest.ably.io/channels/{self.room_code}/messages"
        auth = tuple(self.api_key.split(":"))

        threading.Thread(target=lambda: requests.post(
            url, json={"name": "msg", "data": payload}, auth=auth, timeout=5
        ), daemon=True).start()

        self.input.delete(0, "end")
        self.unfocus_chat()

    def send_system(self, kind, data=""):
        if not self.room_code: return
        payload = f"SYSTEM:{kind}:{self.username}:{self.session_id}:{data}"
        auth = tuple(self.api_key.split(":"))
        threading.Thread(target=lambda: requests.post(
            f"https://rest.ably.io/channels/{self.room_code}/messages",
            json={"name": "sys", "data": payload}, auth=auth, timeout=5
        ), daemon=True).start()

    def host(self):
        self.room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.connect()
        self.write(None, f"--- ROOM CREATED: {self.room_code} ---", True)

    def join(self):
        c = ctk.CTkInputDialog(text="Room Code:", title="Join").get_input()
        if c:
            self.room_code = c.upper()
            self.connect()
            self.write(None, f"--- CONNECTED TO {self.room_code} ---", True)

    def connect(self):
        self.status.configure(text=f"ROOM: {self.room_code}", text_color="#00ff00")
        threading.Thread(target=self.listen, daemon=True).start()
        time.sleep(0.3)
        self.send_system("JOIN")

    def focus_chat(self, e=None):
        self.input.configure(state="normal")
        self.input.focus_set()

    def unfocus_chat(self, e=None):
        self.input.configure(state="disabled")
        self.root.focus_set()

    def move_start(self, e): self.x, self.y = e.x, e.y
    def move_drag(self, e):
        self.root.geometry(f"+{self.root.winfo_x() + e.x - self.x}+{self.root.winfo_y() + e.y - self.y}")

    def init_app(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f: self.api_key = f.read().strip()
            self.ask_username()
        else: self.show_setup()

    def show_setup(self):
        win = ctk.CTkToplevel(self.root)
        win.geometry("350x200")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="ABLY API KEY").pack(pady=10)
        entry = ctk.CTkEntry(win, width=300)
        entry.pack()
        def save():
            self.api_key = entry.get().strip()
            with open("config.txt", "w") as f: f.write(self.api_key)
            win.destroy()
            self.ask_username()
        ctk.CTkButton(win, text="SAVE", command=save).pack(pady=10)

    def ask_username(self):
        d = ctk.CTkInputDialog(text="Username:", title="Login")
        res = d.get_input()
        self.username = res if res else f"User{random.randint(100,999)}"
        self.write(None, f"--- LOGGED IN AS {self.username} ---", True)

    def on_close(self):
        try: self.send_system("LEAVE")
        except: pass
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    PortableChat()
