# 🔐 SSHR

**SSHR (SSH Register)** is a Python tool designed to simplify the management of SSH connections using aliases, allowing you to register, edit, and delete configurations without manually modifying the `~/.ssh/config` file.

---

## 🚀 What is SSHR?

SSHR automates the creation and management of SSH entries, making it easier and more convenient to work with multiple remote connections.

---

## ⚙️ How does it work?

SSHR processes an input in the following format:

```bash
username@host:port
```

And automatically generates an SSH entry like this:

```bash
Host my-server
    HostName 192.168.1.1
    User user
    Port 22
```

---

## 🏁 Main features

SSHR works through command-line flags:

* `-r` → Register a new connection
* `-l` → List saved connections
* `-e` → Edit an existing connection
* `-d` → Delete a connection

> For more details, use the built-in help system.

---

## 📖 Help

The tool includes a help system (`--help`) that explains all available options and their usage.

---

## 🛠️ Project status

* ✅ Connection registration (`-r`) implemented
* ✅ Listing connections (`-l`) implemented
* ✅ Deleting connections (`-d`) implemented
* ⚙️ Editing connections (`-e`) in development
* ⚙️ Help command (`-h`) in development


---

## 💻 Compatibility

SSHR is currently developed and tested on GNU/Linux systems.

Windows support is not implemented yet and is planned for future development.

---

## 🧠 Project philosophy

* Keep things simple and clear
* Automate repetitive tasks
* Avoid unnecessary over-validation
* Give control to the user

---

## 📌 Notes

* SSHR does not replace SSH, it complements it
* It is designed to be a lightweight and practical tool
* Ideal for personal use and learning purposes

---

## 🌍 Languages

This project is also available in other languages:

- 🇺🇸 English (default)
- 🇪🇸 [Español](./docs/README_es.md)
