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

| Flag | Command | Description |
|------|---------|-------------|
| `-r`, `--register` | register | Register a new connection |
| `-l` | list | List connections (compact) |
| `-ll` | list | List connections (detailed) |
| `-d`, `--delete` | delete | Delete a connection (interactive) |
| `-e`, `--edit` | edit | Edit a connection (in development) |
| `--build` | build | Build directory structure |
| `-h`, `--help [topic]` | help | Show general, command, or error help |

---

## 📖 Help

The tool includes a built-in help system with three modes:

```bash
sshr -h                  # General help — shows all commands
sshr -h register         # Command-specific help — shows usage and examples
sshr -h ERR012           # Error help — explains what the error means
```

---

## 🔧 First run

After installation, run `sshr --build` first. It prepares the required config files and directories so SSHR works correctly: it copies the SSHR config files into `~/.config/sshr`, creates `~/.ssh` if needed, and ensures `~/.ssh/config` exists before you start using the tool.

---

## 🛠️ Project status

* ✅ Connection registration (`-r`) implemented
* ✅ Listing connections (`-l`) implemented
* ✅ Deleting connections (`-d`) implemented
* ✅ Build command (`--build`) implemented
* ⚙️ Editing connections (`-e`) in development
* ✅ Help command (`-h`) implemented


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
