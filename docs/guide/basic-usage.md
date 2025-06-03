# Basic Usage

## Starting Meine

To start Meine, open your terminal and type:

```bash
meine
python -m meine
```

This will launch the Terminal User Interface (TUI) with a three-panel layout:
- Left: Directory tree
- Center: File operations and command input
- Right: File preview/information

## Navigation

### Keyboard Navigation

- `↑`, `↓`: Navigate through files and directories
- `←`, `→`: Move between panels
- `Enter`: Open directory or file
- `Backspace`: Go to parent directory
- `Tab`: Switch focus between panels
- `Esc`: Close dialogs or return to previous view

### Mouse Support

Meine supports mouse interaction:
- Click to select files and directories
- Double-click to open
- Right-click for context menu
- Scroll to navigate through lists

## Basic Commands

### File Operations

```bash
# Delete files
del file.txt
rm file1.txt, file2.txt

# Copy files
copy source.txt to destination/
cp multiple*.txt to backup/

# Move files
move old.txt to new/location/
mv *.pdf to documents/

# Rename files
rename oldname.txt as newname.txt
ren doc.txt as document.txt

# Create files/directories
mk newfile.txt
mkdir newfolder
```

### System Commands

```bash
# System information
cpu          # CPU usage and stats
ram          # Memory information
battery      # Battery status
ip           # Network information
gpu          # GPU details

# Environment
env          # Show environment variables
user         # Show user information
```

## File Preview

Meine provides built-in preview support for various file types:

- Text files (`.txt`, `.md`, `.json`, etc.)
- Images (`.png`, `.jpg`, `.gif`)
- Archives (`.zip`, `.tar`, `.gz`)
- And more...

To preview a file, select it in the file browser panel.

## Search and Filter

### Quick Search

Press `/` to activate search mode and type your search term. The results will be filtered in real-time.

### Advanced Search

```bash
search "pattern" folder/     # Search in specific folder
find "text" *.txt           # Search in text files
grep "regex" src/*.py       # Search with regex
```

## Command History

- `↑`, `↓` in the command input to navigate through command history
- `Ctrl+R` to search command history
- History is preserved between sessions

## Configuration

Basic settings can be accessed through:
- The settings panel (`Ctrl+,`)
- Command line options
- Configuration file (`~/.config/meine/config.json`)

