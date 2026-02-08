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
        self.root.attributes("-alpha", 0.90)
        self.root.configure(fg_color="#1a1a1a")
        
        self.api_key = ""
        self.username = ""
        self.room_code = ""
        self.last_msg_id = ""
        self.running = True
        self.triggers = [";", "/"]
        self.blacklisted = ["cp", "gore", "slur", "nazi", "hitler"] 

        self.display = ctk.CTkTextbox(self.root, width=360, height=220, state="disabled", fg_color="#121212")
        self.display.pack(pady=10, padx=10)

        self.input = ctk.CTkEntry(self.root, placeholder_text="Press ; or / to chat...", width=360)
        self.input.pack(pady=5, padx=10)
        self.input.bind("<Return>", self.send)
        self.input.bind("<Button-1>", self.focus_chat)
        self.input.configure(state="disabled")

        self.status = ctk.CTkLabel(self.root, text="F1: HOST | F2: JOIN | ESC: UNLOCK", text_color="gray")
        self.status.pack()

        for k in self.triggers: self.root.bind(f"<KeyPress-{k}>", self.focus_chat)
        self.root.bind("<F1>", lambda e: self.host())
        self.root.bind("<F2>", lambda e: self.join())
        self.root.bind("<Escape>", self.unfocus_chat)
        
        self.root.bind("<ButtonPress-1>", self.move_start)
        self.root.bind("<B1-Motion>", self.move_drag)

        self.init_app()
        self.root.mainloop()

    def apply_filter(self, text):
        original_text = text
        t_lower = text.lower()
        links = r"(http|https|www|\.com|\.net|\.org|\.br|\.gg|\.me|://)"
        if re.search(links, t_lower.replace(" ", "")):
            return "################ (LINK BLOCKED)"

        for word in self.blacklisted:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            if pattern.search(t_lower):
                return "******** (INAPPROPRIATE CONTENT)"
        
        return original_text

    def send(self, e=None):
        raw_msg = self.input.get().strip()
        if not raw_msg or not self.room_code: return
        msg = self.apply_filter(raw_msg)
        self.write(f"{self.username}: {msg}")
        url = f"https://rest.ably.io/channels/{self.room_code}/messages"
        auth = tuple(self.api_key.split(":"))
        threading.Thread(target=lambda: requests.post(url, json={"name":"msg", "data":f"{self.username}: {msg}"}, auth=auth), daemon=True).start()
        self.input.delete(0, 'end')
        self.unfocus_chat()

    def listen(self):
        url = f"https://rest.ably.io/channels/{self.room_code}/history"
        auth = tuple(self.api_key.split(":"))
        try:
            r = requests.get(url, params={'limit':1}, auth=auth)
            if r.status_code == 200 and r.json():
                self.last_msg_id = r.json()[0].get('id')
        except: pass

        while self.running:
            try:
                r = requests.get(url, params={'limit':1}, auth=auth)
                if r.status_code == 200:
                    data = r.json()
                    if data:
                        msg_obj = data[0]
                        if msg_obj.get('id') != self.last_msg_id:
                            self.last_msg_id = msg_obj.get('id')
                            content = str(msg_obj.get('data'))
                            if not content.startswith(f"{self.username}:"):
                                self.write(content)
            except: pass
            time.sleep(0.5)

    def init_app(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f: self.api_key = f.read().strip()
            self.ask_username()
        else: self.show_setup_screen()

    def show_setup_screen(self):
        self.setup_win = ctk.CTkToplevel(self.root)
        self.setup_win.geometry("350x230")
        self.setup_win.title("Setup")
        self.setup_win.attributes("-topmost", True)
        ctk.CTkLabel(self.setup_win, text="ENTER API KEY", font=("Arial", 12, "bold")).pack(pady=10)
        self.key_entry = ctk.CTkEntry(self.setup_win, width=300)
        self.key_entry.pack()
        self.key_entry.bind("<KeyRelease>", self.check_key)
        self.save_btn = ctk.CTkButton(self.setup_win, text="SAVE", state="disabled", command=self.save_key)
        self.save_btn.pack(pady=10)

    def check_key(self, e):
        if ":" in self.key_entry.get(): self.save_btn.configure(state="normal")
        else: self.save_btn.configure(state="disabled")

    def save_key(self):
        with open("config.txt", "w") as f: f.write(self.key_entry.get().strip())
        self.api_key = self.key_entry.get().strip()
        self.setup_win.destroy()
        self.ask_username()

    def ask_username(self):
        d = ctk.CTkInputDialog(text="Username:", title="Login")
        name = d.get_input()
        self.username = name if name else f"User{random.randint(100, 999)}"
        self.write(f"--- Session: {self.username} ---")

    def write(self, txt):
        self.display.configure(state="normal")
        self.display.insert("end", txt + "\n")
        self.display.see("end")
        self.display.configure(state="disabled")

    def host(self):
        self.room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.connect()

    def join(self):
        c = ctk.CTkInputDialog(text="Room Code:", title="Join").get_input()
        if c: 
            self.room_code = c.upper()
            self.connect()

    def connect(self):
        self.status.configure(text=f"ROOM: {self.room_code}", text_color="#00ff00")
        threading.Thread(target=self.listen, daemon=True).start()

    def focus_chat(self, e=None):
        self.input.configure(state="normal")
        self.input.focus_set()

    def unfocus_chat(self, e=None):
        self.input.configure(state="disabled")
        self.root.focus_set()

    def move_start(self, e): self.x, self.y = e.x, e.y
    def move_drag(self, e):
        nx, ny = self.root.winfo_x() + (e.x - self.x), self.root.winfo_y() + (e.y - self.y)
        self.root.geometry(f"+{nx}+{ny}")

if __name__ == "__main__":
    PortableChat()