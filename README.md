# 🌐 Portable Chat

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Technology](https://img.shields.io/badge/powered%20by-Ably-orange)

**The Universal Overlay for "Chatless" Games & Restricted Apps.**

`Portable Chat` is a lightweight, transparent overlay application designed to stay on top of any window. It’s the perfect solution for real-time communication when built-in game chats are non-existent, restricted, or simply terrible.

---

## ✨ Key Features

* **Floating Overlay:** Stays on top of your game (Borderless/Windowed mode).
* **Privacy First:** Decentralized communication using your own Ably infrastructure.
* **Zero Alt-Tab:** Use hotkeys to focus and unfocus instantly.
* **Room System:** Easy 6-digit codes to gather your squad.

---

## ⚠️ CRITICAL: Connection & Safety

> [!IMPORTANT]  
> **"If you entered an API Key but cannot see your friends, the keys are different."**

For the chat to function, **everyone in your group MUST use the exact same API Key**. The application isolates traffic based on this key. 
* **Key A Users:** Talk to Key A users.
* **Key B Users:** Talk to Key B users.
* **Security:** ONLY share your API Key with people you trust!

---

## ⚙️ Setup Instructions

This app uses [Ably](https://ably.com) (Free Tier) to handle lightning-fast messaging without a middleman server.

1.  **Get your API Key:**
    * Sign up at [Ably.com](https://ably.com).
    * Go to **Dashboard** -> **API Keys**.
    * Copy the `Root Key` (Format: `xxxxxx.xxxxxx:xxxxxxxxxxxx`).
2.  **First Launch:**
    * Run `PortableChat.exe`.
    * Enter your key in the setup screen (validated in real-time).
    * A `config.txt` will be created locally.
3.  **Sync with Friends:**
    * Send your friends the **same key** and a **Room Code**.

---

## ⌨️ Controls & Hotkeys

| Action | Key |
| :--- | :--- |
| **Focus Chat / Start Typing** | `;` or `/` |
| **Unfocus / Return to Game** | `Esc` |
| **Host New Room** | `F1` (Generates 6-digit code) |
| **Join Existing Room** | `F2` (Enter friend's code) |
| **Move Chat** | `Click & Drag` background |

---

## 🛠️ Built With

* [Ably](https://ably.com/) - Real-time Pub/Sub messaging.
* *Add your other frameworks here (e.g., Python/Tkinter, Electron, C#, etc.)*

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
