import os
import asyncio
from pathlib import Path
from typing import Dict, Optional, Set

from rich.panel import Panel
from textual.events import Click
from textual.screen import Screen
from textual.widgets import DirectoryTree, Input, RichLog, Header

from meine.exceptions import InfoNotify
from meine.ui_handler import CLI
from meine.widgets.containers import (
    Background_process_container,
    Container,
    Directory_tree_container,
)
from meine.screens.textarea import MeineTextAreaScreen
from meine.widgets.input import MeineInput
from meine.utils.file_manager import load_random_quote


class HomeScreen(Screen):
    """Main home screen of the application."""

    AUTO_FOCUS = "#command-input"
    CSS_PATH: Path = Path(__file__).parent.parent / "tcss/app.tcss"

    def __init__(self, name: Optional[str] = None, id: Optional[str] = None, classes: Optional[str] = None):
        self.HISTORY_INDEX = len(self.app.HISTORY)
        self.si: Dict[str, Path] = {}
        self._command_tasks: Set[asyncio.Task] = set()
        super().__init__(name, id, classes)

    def compose(self):
        """Compose the screen layout."""
        self.inputconsole = MeineInput(
            placeholder="Enter command.... [/ to jump here]",
            id="command-input",
            history=self.app.HISTORY,
            history_index=self.HISTORY_INDEX,
        )
        self.rich_log = RichLog(id="output", highlight=True)
        self.directory_tree_container = Directory_tree_container(
            classes="-hidden", id="directory-tree-container"
        )
        self.directory_tree_container.styles.dock = self.app.SETTINGS["directory-tree-dock"]
        self.Dtree = self.directory_tree_container.dtree
        self.bgprocess = Background_process_container(classes="-hidden")
        self.input_output_container = Container(self.inputconsole, self.rich_log, id="IO")

        yield Header()
        with Container(id="home-screen"):
            yield self.input_output_container
            yield self.directory_tree_container
            yield self.bgprocess

    def _on_mount(self) -> None:
        """Set up the screen on mount."""
        self.title = load_random_quote()

    def key_ctrl_b(self) -> None:
        """Toggle background process visibility."""
        self.bgprocess.toggle_class("-hidden")

    def handle_files_click_input(self, widget) -> None:
        """Handle file selection in the directory tree."""
        try:
            if not self.Dtree.cursor_node:
                return

            selected_node = self.Dtree.cursor_node.data.path
            name = f"'{selected_node.name}'" if " " in selected_node.name else selected_node.name
            input_text = self.inputconsole.value.strip()

            # Handle file selection logic
            if name not in self.si:
                separator = " " if not input_text or not self.si else ","
                self.inputconsole.value = f"{input_text}{separator}{name}".strip()
                self.si[name] = selected_node
            else:
                del self.si[name]
                self.inputconsole.value = input_text.replace(f",{name}", "").replace(name, "").strip()

        except Exception as e:
            raise InfoNotify(f"Error handling file selection: {e}")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command input submission."""
        if not event.value.strip() or event.input.id != "command-input":
            return

        cmd = event.value.strip()
        try:
            if cmd.startswith("cd "):
                await self._handle_cd_command(cmd[3:])
            elif cmd == "cwd":
                self.notify(message=str(Path.cwd()), title="Current working directory")
            elif cmd == "clear":
                self.clear_rich_log()
            else:
                task = asyncio.create_task(self.execute_command(cmd))
                self._command_tasks.add(task)
                task.add_done_callback(self._command_tasks.discard)

            self.app.HISTORY.append(cmd)
            self.HISTORY_INDEX = len(self.app.HISTORY)
            event.input.value = ""

        except InfoNotify as e:
            self.notify(message=str(e), title="Error", severity="error")
        except Exception as e:
            raise InfoNotify(f"Command execution failed: {e}")

    async def _handle_cd_command(self, path_str: str) -> None:
        """Handle cd command with proper error handling."""
        try:
            path = Path(path_str).resolve()
            if not path.exists():
                raise InfoNotify(f"Path does not exist: {path}")
            if not path.is_dir():
                raise InfoNotify(f"Not a directory: {path}")

            await self.change_directory(path)
            self.notify(message=str(path), title="Changed directory")

        except PermissionError:
            raise InfoNotify(f"Permission denied: {path_str}")

    def key_ctrl_r(self) -> None:
        """Reload directory tree."""
        try:
            self.Dtree.reload()
        except Exception as e:
            raise InfoNotify(f"Failed to reload directory tree: {e}")

    def clear_rich_log(self) -> None:
        """Clear the output log."""
        self.rich_log.clear()

    async def execute_command(self, cmd: str) -> None:
        """Execute a command asynchronously."""
        try:
            result = await CLI(cmd)
            if not result:
                return

            if not isinstance(result, Panel):
                theme = self.app.current_theme
                self.rich_log.write(Panel(result, expand=False, style=theme.primary))
            else:
                self.rich_log.write(result)

        except InfoNotify:
            raise
        except Exception as e:
            raise InfoNotify(f"Command execution failed: {e}")

    def key_ctrl_d(self) -> None:
        """Toggle directory tree visibility."""
        self.directory_tree_container.toggle_class("-hidden")

    async def change_directory(self, cmdpath: Path) -> None:
        """Change current directory with proper error handling."""
        try:
            dtree = self.query_one("#directory-tree", DirectoryTree)
            dtree.path = cmdpath
            os.chdir(cmdpath)
            self.si.clear()  # Clear selected items when changing directory
        except FileNotFoundError:
            raise InfoNotify(f"Directory not found: {cmdpath}")
        except PermissionError:
            raise InfoNotify(f"Permission denied: {cmdpath}")
        except Exception as e:
            raise InfoNotify(f"Error changing directory: {e}")

    def on_click(self, event: Click) -> None:
        """Handle click events on the directory tree."""
        if event.widget.id != "directory-tree":
            return

        try:
            if event.ctrl:
                self.handle_files_click_input(event.widget)
                return

            tree = self.query_one("#directory-tree", DirectoryTree)
            if not tree.cursor_node:
                return

            selected_node = tree.cursor_node.data.path
            if selected_node == tree.root.data.path:
                self._change_directory_sync(selected_node.parent)
            elif selected_node.is_dir():
                self._change_directory_sync(selected_node)
            elif selected_node.is_file():
                self._handle_file_click(selected_node)

        except InfoNotify:
            raise
        except Exception as e:
            raise InfoNotify(f"Error handling click: {e}")

    def _change_directory_sync(self, path: Path) -> None:
        """Synchronously change directory with error handling."""
        try:
            tree = self.query_one("#directory-tree", DirectoryTree)
            tree.path = path
            os.chdir(path)
        except Exception as e:
            raise InfoNotify(f"Failed to change directory: {e}")

    def _handle_file_click(self, file_path: Path) -> None:
        """Handle file click with proper error handling."""
        try:
            if self._is_text_file(file_path):
                self.app.push_screen(
                    MeineTextAreaScreen(filepath=file_path, id="textarea-screen")
                )
            else:
                raise InfoNotify("Unsupported file format")
        except Exception as e:
            raise InfoNotify(f"Error opening file: {e}")

    @staticmethod
    def _is_text_file(file_path: Path, block_size: int = 512) -> bool:
        """Check if a file is text-based."""
        try:
            with open(file_path, "rb") as file:
                chunk = file.read(block_size)
                if b"\x00" in chunk:
                    return False
                try:
                    chunk.decode("utf-8")
                    return True
                except UnicodeDecodeError:
                    return False
        except Exception as e:
            raise InfoNotify(f"Error checking file type: {e}")

    def key_slash(self) -> None:
        """Focus the command input when slash is pressed."""
        if self.focused.id != "command-input":
            self.inputconsole.focus()
            self.inputconsole.select_on_focus = False

    async def on_worker_failed(self, event) -> None:
        """Handle worker failures."""
        raise InfoNotify(f"Worker failed: {event}")
