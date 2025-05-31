from pathlib import Path

from textual.screen import ModalScreen
from textual.widgets import MarkdownViewer


HELP_MANUAL = """\

# Directory Tree

## Key Bindings


- **Ctrl + D**: Toggle the directory tree.
- **Left Arrow Key**: Move to the parent directory.
- **Right Arrow Key** or **Mouse Click**: Move to the currently focused directory.
- **Up Arrow Key / Down Arrow Key**: Navigate up or down through directories.
- **Home Key**: Move directly to the home directory.
- **Ctrl + Click**: Copy the name of the directory or file to the input console.
- **Tab**: Refresh the directory tree.

## Note

- Changing the directory in the directory tree will also update the **current working directory**.
  - **Example**: Using the directory tree to change a directory is equivalent to executing the `cd` command in the terminal.

---

# Input Console Help

## Command Reference

### **Delete Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Single     | `d`, `rm`, `r`, `del <file/folder name>`      |
| Multiple   | `d`, `rm`, `r`, `del <file1>, <file2>, ...`   |

### **Create Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Single     | `mk (or) create <filename>`, `mkdir|mkd <foldername>`|
| Multiple   | `mk (or) create <filename1>, <filename2>, ...`, `mkdir|mkd <foldername1>, <foldername2>, ...` |

### **Rename Command**

| Action     | Command                                        |
|-------------|-----------------------------------------------|
| Single     | `rn (or) rename <oldname> as <newname>`             |
| Multiple   | `rn (or) rename <oldname1>, <oldname2>, ... as <newname1>, <newname2>, ...` |

### **Copy Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Single     | `cp (or) c (or) copy <source> to <destination>`         |
| Multiple   | `cp (or) c (or) copy <source1>, <source2>, ... to <destination>` |

### **Move Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Single     | `mv (or) m (or) move <source> to <destination>`         |
| Multiple   | `mv (or) m (or) move <source1>, <source2>, ... to <destination>` |

### **Search Text Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Folder     | `search (or) find (or) where "text" <folder path>`      |
| File       | `search (or) find (or) where "text" <file path>`        |

---

## System Commands

| Command | Description                              |
|---------|------------------------------------------|
| `ram`   | Display RAM details                      |
| `cpu`   | Display CPU details                      |
| `gpu`   | Display GPU details                      |
| `battery` | Display battery status                  |
| `charge` | Display charging status                 |
| `ip`    | Display IP address                       |
| `disk`  | Display disk information                 |
| `time`  | Display current system time              |
| `os`    | Display operating system information     |
| `sys`   | Display system information               |
| `user,me` | Display current user information        |
| `net`   | Display network details                  |
| `env`   | Display environmental variables          |

 """


class HelpScreen(ModalScreen[None]):

    CSS_PATH = Path(__file__).parent.parent / "tcss/help.tcss"

    def compose(self):

        yield MarkdownViewer(HELP_MANUAL)
