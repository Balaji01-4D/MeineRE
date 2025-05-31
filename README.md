
# meine

<p align="center">
  <img src="https://socialify.git.ci/Balaji01-4D/meine/image?description=1&font=Jost&language=1&name=1&owner=1&pattern=Floating+Cogs&theme=Auto" alt="project-banner">
</p>

> ⚙️ **meine** is a cross-platform, regex-powered command-line interface for automating file operations, system control, and archive manipulation—delivered in a beautiful terminal UI.
> Modular, asynchronous, and extensible. Built for those who want raw power in a refined shell.

---

## 🚀 Features

- **🔍 Regex-Based Command Parsing**
  Use intuitive commands to delete, copy, move, rename, search, and create files or folders.

- **🗂️ TUI Directory Navigator**
  Browse your filesystem in a reactive terminal UI—keyboard and mouse supported.

- **💬 Live Command Console**
  A built-in shell for interpreting commands and reflecting state changes in real time.

- **⚡ Asynchronous & Modular**
  Built with `asyncio`, `aiofiles`, `py7zr`, and modular architecture for responsive performance.

- **🎨 Theming & Config**
  CSS-powered themes, JSON-based user preferences, and dynamic runtime settings.

- **📊 System Dashboard**
  Real-time system insights via one-liner commands:
  `cpu`, `ram`, `gpu`, `battery`, `ip`, `user`, `env`, and more.

- **🧩 Plugin Ready**
  Drop in your own Python modules to extend functionality without altering core logic.

---

## 📸 Screenshots

<p float="left">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/opening.png" width="100%" alt="Opening screen">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/input.png" width="100%" alt="Input shell">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/texteditor.png" width="100%" alt="Text editor">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/settings.png" width="100%" alt="Settings screen">
</p>

---

## 🛠️ Installation

**Install via pip**
> Requires Python 3.10+

```bash
pip install meine
```

Or clone the repo:

```bash
git clone https://github.com/Balaji01-4D/meine
cd meine
pip install .
```

---

## 🔤 Regex-Based Commands

| Action      | Syntax Example                                  |
|-------------|--------------------------------------------------|
| **Delete**  | `del file.txt`  ·  `rm file1.txt, file2.txt`     |
| **Copy**    | `copy a.txt to b.txt` · `cp a1.txt, a2.txt to d/`|
| **Move**    | `move a.txt to d/` · `mv f1.txt, f2.txt to ../`  |
| **Rename**  | `rename old.txt as new.txt`                      |
| **Create**  | `mk file.txt` · `mkdir folder1, folder2`         |
| **Search**  | `search "text" folder/` · `find "term" notes.md` |

---

## 🧱 Project Structure

```text
meine/
├── meine/              # Core package
│   ├── app.py          # Main entry point
│   ├── themes.py       # Theme loader
│   ├── runtime_config.json
│   ├── tcss/           # Terminal CSS files
│   ├── resources/      # JSON static data
│   ├── widgets/        # UI components
│   ├── screens/        # Screen layouts (text editor, dashboard, etc.)
│   ├── Actions/        # File and system command handlers
│   └── utils/          # Helper functions
├── pyproject.toml      # PEP-517/518 build config
├── README.md
├── requirements.txt
└── LICENSE
```

---

## ✨ Roadmap

- [ ] Plugin Manager System
- [ ] Git & GitHub integration
- [ ] Built-in Task Scheduler
- [ ] Voice Command Support
- [ ] Remote SSH Execution

---

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

To contribute:

```bash
git clone https://github.com/Balaji01-4D/meine
cd meine
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 💬 Connect

Got feedback, suggestions, or just wanna say hi?

- Instagram: [__balaji.j__](https://www.instagram.com/__balaji.j__/)
- GitHub Issues: [meine Issues](https://github.com/Balaji01-4D/meine/issues)

---
