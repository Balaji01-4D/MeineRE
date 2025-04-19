<h1 align="center" id="title">MeineRe</h1>

<p align="center"><img src="https://socialify.git.ci/Balaji01-4D/MeineRE/image?description=1&amp;font=Jost&amp;language=1&amp;name=1&amp;owner=1&amp;pattern=Floating+Cogs&amp;theme=Auto" alt="project-image"></p>

<p id="description">MeineRE is a platform-independent regex-powered command-line interface designed for automation system control file manipulation and compression tasks. Built with modularity in mind MeineRE routes user input through powerful regex dispatching to specialized handlers. It provides a responsive TUI using the Textual framework and supports real-time command parsing dynamic configuration and integration of custom plugins. Whether you're navigating your filesystem compressing archives managing system processes or extending with new modules MeineRE gives you full control—all from one elegant command shell.</p>


<h2>Project Screenshots:</h2>
<p></p>
<img src="https://github.com/Balaji01-4D/MeineRE/blob/main/img/opening.png" alt="project-screenshot" width="100%" height="50%">
<img src="https://github.com/Balaji01-4D/MeineRE/blob/main/img/input.png" alt="project-screenshot" width="100%" height="50%">
<img src="https://github.com/Balaji01-4D/MeineRE/blob/main/img/texteditor.png" alt="project-screenshot" width="100%" height="50%">
<img src="https://github.com/Balaji01-4D/MeineRE/blob/main/img/settings.png" alt="project-screenshot" width="100%" height="50%">

<h2>🛠️ Installation Steps:</h2>

<p>Using PIP</p>

```
pip install MeineRE
```



---

### 🔍 Core Features

- **Regex-Based Command Parsing** – Delete, rename, move, copy, search, and create files or folders using natural terminal language.
- **Directory Tree UI** – Navigate your filesystem using arrow keys, mouse clicks, or keybinds (e.g., `Ctrl+D`, `Home`, `Tab`) with real-time directory state sync.
- **Command Console** – A built-in input console interprets your commands and updates state like a shell.
- **Asynchronous Architecture** – Powered by `asyncio`, `aiofiles`, `py7zr`, and other async modules for non-blocking operations.
- **Custom Themes & Configs** – CSS-based theming, JSON-based runtime and user preferences stored and managed per user.
- **System Info Dashboard** – Query system info with simple commands like `cpu`, `gpu`, `ram`, `battery`, `ip`, `disk`, `user`, `env`, and more.

### 💡 Regex-Based Commands

| Action      | Syntax Example                                  |
|-------------|--------------------------------------------------|
| **Delete**  | `del file.txt`, `rm file1.txt, file2.txt`        |
| **Copy**    | `copy a.txt to b.txt`, `cp a1.txt, a2.txt to d/` |
| **Move**    | `move a.txt to d/`, `mv f1.txt, f2.txt to ../`   |
| **Rename**  | `rename old.txt as new.txt`                      |
| **Create**  | `mk file.txt`, `mkdir folder1, folder2`          |
| **Search**  | `search "text" folder/`, `find "term" notes.md`  |

### 📦 Project Layout

```shell
MeineRE/
├── Meine/              # Core package
│   ├── app.py          # Entry point
│   ├── themes.py       # Theme loader
│   ├── runtime_config.json
│   ├── tcss/           # Custom CSS
│   ├── resources/      # Static JSON resources
│   ├── widgets/        # UI components
│   ├── screens/        # Screen layouts
│   ├── Actions/        # File & system operations
│   └── utils/          # Utility functions
├── pyproject.toml
├── README.md
├── requirements.txt
└── LICENSE
```

---

