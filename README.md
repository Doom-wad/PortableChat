# 🌐 Portable Chat

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Windows](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows)
![Android](https://img.shields.io/badge/platform-Android-3DDC84?logo=android)
![Technology](https://img.shields.io/badge/powered%20by-Ably-orange)

**The Universal Chat Overlay for Gamers.** `Portable Chat` is a lightweight, cross-platform tool designed for games that lack a built-in chat system. Whether you are on PC or Mobile, stay connected with your squad without losing sight of the action.

---

## 📱 Platform Specifics

### 💻 Windows Desktop
A dedicated semi-transparent window that stays **Always on Top**. Perfect for borderless or windowed gaming.

### 🤖 Android Mobile
Designed to work perfectly using the Android **"Pop-up View"** or **"Split Screen"** features.
* **How to use on Mobile:** Open the app, go to your "Recent Apps" screen, tap the app icon, and select **"Open in pop-up view"**. This allows the chat to float over any mobile game!

---

## ✨ Key Features

* **Cross-Platform:** Chat between PC and Android users in the same room.
* **Privacy First:** Your messages travel through your own Ably infrastructure.
* **Minimalist UI:** Low resource usage, no lag, no bloatware.
* **Quick Rooms:** Join your friends in seconds with 6-digit codes.

---

## ⚠️ CRITICAL: Connection & Safety

> [!IMPORTANT]  
> **"API Key Mismatch = Invisible Chat"**
> 
> To communicate, **everyone in the group MUST use the exact same API Key**. The application isolates traffic based on this key. 
> * **Security:** NEVER share your API Key with strangers!

---

## ⚙️ Setup Instructions

This app uses [Ably](https://ably.com) (Free Tier) for real-time messaging.

1.  **Get your API Key:**
    * Sign up at [Ably.com](https://ably.com).
    * Copy the `Root Key` from your Dashboard.
2.  **Installation:**
    * **PC:** Run `PortableChat.exe`. Key is saved in `config.txt`.
    * **Android:** Install the `.apk` and enter the key in the main screen.
3.  **Join the Squad:**
    * One person presses **F1 (PC)** or **Host (Android)** to get a code.
    * Everyone else enters that code via **F2 (PC)** or **Join (Android)**.

---

## ⌨️ Desktop Hotkeys

| Action | Key |
| :--- | :--- |
| **Focus Chat / Type** | `;` or `/` |
| **Generate Room Code** | `F1` |
| **Enter Room Code** | `F2` |

---

## 🤝 Contributing

Got an idea to make it better? 
1. Fork the Project.
2. Create your Feature Branch.
3. Open a Pull Request.
