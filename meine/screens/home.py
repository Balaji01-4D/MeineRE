import os
import asyncio
from pathlib import Path

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

    AUTO_FOCUS = "#command-input"

    CSS_PATH: Path = Path(__file__).parent.parent / "tcss/app.tcss"

    def __init__(self, name=None, id=None, classes=None):
        self.HISTORY_INDEX = len(self.app.HISTORY)
        self.si = {}
        super().__init__(name, id, classes)

    def compose(self):
        self.inputconsole = MeineInput(
            placeholder="Enter command.... [/ to jump here]",
            id="command-input",
            history=self.app.HISTORY,
            history_index=self.HISTORY_INDEX,
        )
        self.rich_log = RichLog(id="output",highlight=True)

        self.directory_tree_container = Directory_tree_container(
            classes="-hidden", id="directory-tree-container"
        )
        self.directory_tree_container.styles.dock = self.app.SETTINGS[
            "directory-tree-dock"
        ]

        self.Dtree = self.directory_tree_container.dtree
        self.bgprocess = Background_process_container(classes="-hidden")
        self.input_output_container = Container(
            self.inputconsole, self.rich_log, id="IO"
        )

        yield Header()
        with Container():
            yield self.input_output_container
            yield self.directory_tree_container
            yield self.bgprocess

    def _on_mount(self) -> None:
        self.title = load_random_quote()

    def key_ctrl_b(self):
        """
        Handles the Ctrl+B key press event.

        Toggles the visibility of the background process by switching the
        "-hidden" class, which shows or hides the background process element.
        """
        self.bgprocess.toggle_class("-hidden")

    def handle_files_click_input(self, widget) -> None:

        def qoutes_for_spaced_name(name: str) -> None:
            """returns quoted string if there is whitespace otherwise same"""
            return f"'{name}'" if (" " in name) else name

        try:
            selected_node = self.Dtree.cursor_node.data.path
            name = qoutes_for_spaced_name(selected_node.name)
            input_text = self.inputconsole.value

            if not self.si and name not in input_text:
                self.inputconsole.value = f"{input_text.strip()} {name}"
                self.si[name] = selected_node
            elif name in self.si and name not in input_text:
                if len(self.si) == 1:
                    self.inputconsole.value = f"{input_text} {name}"
                else:
                    if " " in input_text:
                        self.inputconsole.value = f"{input_text},{name}"
                    else:
                        self.inputconsole.value = f"{input_text} {name}"

            elif self.si and name not in input_text:
                self.inputconsole.value = f"{input_text.strip()},{name}"
                self.si[name] = selected_node
            elif not self.si and name in input_text:
                self.inputconsole.value = input_text.replace(name, "")
            else:
                del self.si[name]
                if f",{name}" in input_text:
                    self.inputconsole.value = input_text.replace(f",{name}", "")
                else:
                    self.inputconsole.value = input_text.replace(name, "")

        except Exception as e:
            self.rich_log.write(f"error clicks {e}")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        try:
            cmd = event.value.strip()
            if cmd and event.input.id == "command-input":
                try:
                    if "cd " in cmd:
                        cmdpath = cmd.replace("cd ",'')
                        cmdpath = Path(cmdpath)
                        if cmdpath.is_dir():
                            self.app.run_worker(
                                self.change_directory(cmdpath),
                                name="cd_worker",
                                description="Change Directory",
                            )
                            self.notify(
                                message=f"{str(cmdpath.resolve())}",
                                title="changed directory",
                            )

                        else:
                            message = (
                                f"{cmdpath} is file"
                                if cmdpath.is_file()
                                else f"{cmdpath} Not Found"
                            )
                            self.notify(message=message, severity="error")

                    elif "cwd" in cmd:
                        self.notify(
                            message=f"{os.getcwd()}",
                            title="Current working directory",
                        )
                    elif "clear" in cmd:
                        self.clear_rich_log()
                    else:
                        self.app.run_worker(
                            self.execute_command(cmd),
                            name="cmd_worker",
                            description=f"Executing: {cmd}",
                        )
                except Exception as e:
                    self.rich_log.write(f"[error] {str(e)}")

            self.app.HISTORY.append(cmd)
            self.HISTORY_index = len(self.app.HISTORY)
            event.input.value = ""

        except PermissionError as e:
            None

    def key_ctrl_r(self) -> None:
        self.Dtree.reload()


    def clear_rich_log(self) -> None:
        self.rich_log.clear()

    async def execute_command(self, cmd: str) -> None:
        try:
            self.executable = asyncio.create_task(CLI(cmd))
            result = await self.executable
            if result:
                if not isinstance(result, Panel):
                    theme = self.app.current_theme
                    self.rich_log.write(Panel(result, expand=False, style=theme.primary))
                else:
                    self.rich_log.write(result)
        except InfoNotify as e:
            self.notify(message=e.message, title="ERROR", severity="error")
        except Exception as e:
            self.rich_log.write(f"[error] Command execution failed: {str(e)}")

    def key_ctrl_d(self) -> None:
        """
        Handles the Ctrl+D key press event.

        Toggles the visibility of the directory tree container by switching the
        "-hidden" class, which shows or hides the directory tree element.
        """
        self.directory_tree_container.toggle_class("-hidden")

    async def change_directory(self, cmdpath: Path) -> None:
        try:
            dtree = self.query_one("#directory-tree", DirectoryTree)
            dtree.path = cmdpath.resolve()
            os.chdir(cmdpath)
            self.si = {}
        except FileNotFoundError as e:
            self.rich_log.write(f"error {e}")
        except PermissionError:
            self.rich_log.write("error Permission Denied")
        except Exception as e:
            self.rich_log.write(f"error Error changing directory: {e}")

    def on_click(self, event: Click) -> None:
        try:
            if event.widget.id == "directory-tree" and event.ctrl:
                self.handle_files_click_input(event.widget)
            elif event.widget.id == "directory-tree":
                tree = self.query_one("#directory-tree", DirectoryTree)
                selected_node = tree.cursor_node.data.path
                if selected_node == tree.root.data.path:
                    tree.path = selected_node.parent
                    os.chdir(tree.path)
                elif selected_node.is_dir():
                    tree.path = selected_node
                    os.chdir(tree.path)
                elif selected_node.is_file():
                    if self.is_text_file(selected_node):
                        self.app.push_screen(
                            MeineTextAreaScreen(
                                filepath=selected_node, id="textarea-screen"
                            )
                        )
                    else:
                        self.notify("unsupported file format")
                else:
                    None

        except PermissionError:
            self.notify(title="Error", message="Permission Denied", severity="error")
        except:
            None

    async def on_worker_failed(self, event) -> None:
        """Handle worker failures."""
        self.rich_log.write(f"[error] Worker failed: {event}")

    def is_text_file(self, file_path: str | Path | os.PathLike, block_size=512) -> bool:
        """detects the file is text based or not"""
        try:
            with open(file_path, "rb") as file:
                chunk = file.read(block_size)

                if b"\x00" in chunk:
                    return False

                try:
                    chunk.decode("utf-8")
                except UnicodeDecodeError:
                    return False

                return True
        except Exception:
            return False


    def key_slash(self):
        if not self.focused.id == "command-input":
            self.inputconsole.focus()
            self.inputconsole.select_on_focus = False




    # def handle_files_click_input(self, widget):
    #     def quotes_for_spaced_name(name: str):
    #         """Add quotes around names containing spaces."""
    #         return f"'{name}'" if ' ' in name else name

    #     try:
    #         # Retrieve DirectoryTree and the currently selected file node
    #         Dtree = self.query_one('#dt', DirectoryTree)
    #         selected_node = Dtree.cursor_node.data.path
    #         name = quotes_for_spaced_name(selected_node.name)  # Format name
    #         input_text = self.inputconsole.value.strip()

    #         # Extract the mandatory command
    #         parts = input_text.split(' ', 1)
    #         command = parts[0] if parts else ""  # Get command or empty string
    #         input_items = [item.strip() for item in (parts[1] if len(parts) > 1 else "").split(',') if item.strip()]

    #         # Add/remove the clicked filepath, ensuring no duplicates or errors
    #         if name not in input_items:  # Add to the input field
    #             input_items.append(name)
    #             self.si[name] = selected_node
    #         elif name in input_items:  # Remove if it exists
    #             input_items.remove(name)
    #             del self.si[name]

    #         # Validate the manually typed paths
    #         valid_items = []
    #         for item in input_items:
    #             if item in self.si or item == name:  # Check if valid or matches selected
    #                 valid_items.append(item)
    #             else:  # Ignore invalid items but log them for debugging
    #                 self.rich_log.write(f"Warning: Ignored invalid item '{item}'")

    #         # Reconstruct the inputconsole
    #         self.inputconsole.value = f"{command} {', '.join(valid_items)}".strip()

    #     except Exception as e:
    #         self.rich_log.write(f"Error in handle_files_click_input: {e}")
