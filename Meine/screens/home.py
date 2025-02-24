import os
import asyncio
from pathlib import Path

from rich.panel import Panel
from textual.binding import Binding
from textual.events import Click
from textual.screen import Screen
from textual.widgets import DataTable, DirectoryTree, Input, RichLog

from Meine.exceptions import ErrorNotify, InfoNotify, WarningNotify
from Meine.logger_config import logger
from Meine.main import CLI
from Meine.utils.file_editor import save_history
from Meine.utils.file_loaders import load_history
from Meine.widgets.containers import (
    Background_process_container,
    Container,
    Directory_tree_container,
)
from Meine.screens.textarea import MeineTextAreaScreen
from Meine.widgets.input import MeineInput


class HomeScreen(Screen[None]):

    AUTO_FOCUS = "#command-input"

    CSS_PATH = Path(__file__).parent.parent / "tcss/app.css"

    HISTORY = load_history()
    HISTORY_INDEX = len(HISTORY)

    BINDINGS = [
        Binding("ctrl+d", "toggle_sidebar", show=False, priority=True),
    ]

    def __init__(self, name=None, id=None, classes=None):
        self.si = {}
        super().__init__(name, id, classes)

    def compose(self):
        self.inputconsole = MeineInput(
            placeholder="Enter command....",
            id="command-input",
            history=self.HISTORY,
            history_index=self.HISTORY_INDEX,
        )
        self.rich_log = RichLog(id="output")

        self.sidebar = Directory_tree_container(
            classes="-hidden", id="directory-tree-container"
        )
        self.sidebar.styles.dock = self.app.SETTINGS["directory-tree-dock"]

        self.Dtree = self.sidebar.dtree
        self.bgprocess = Background_process_container(classes="-hidden")
        self.IO_container = Container(self.rich_log, self.inputconsole, id="IO")

        yield self.IO_container
        yield self.sidebar
        yield self.bgprocess

    def key_ctrl_b(self):
        self.bgprocess.toggle_class("-hidden")

    def handle_files_click_input(self, widget):

        def qoutes_for_spaced_name(name: str):
            return f"'{name}'" if (" " in name) else name

        try:
            selected_node = self.Dtree.cursor_node.data.path
            name = qoutes_for_spaced_name(selected_node.name)
            input_text = self.inputconsole.value

            if not self.si and name not in input_text:  # add name
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

            elif self.si and name not in input_text:  # add name
                self.inputconsole.value = f"{input_text.strip()},{name}"
                self.si[name] = selected_node
            elif not self.si and name in input_text:  # remove name
                """if user typed by his own"""
                self.inputconsole.value = input_text.replace(name, "")
            else:
                del self.si[name]
                if f",{name}" in input_text:
                    self.inputconsole.value = input_text.replace(f",{name}", "")
                else:
                    self.inputconsole.value = input_text.replace(name, "")

        except Exception as e:
            self.rich_log.write(f"error clicks {e}")

            logger.error(
                f"{e} Function: {self.handle_files_click_input.__name__} in {Path(__file__).name}"
            )

    async def on_input_submitted(self, event: Input.Submitted):
        try:
            cmd = event.value.strip()
            try:
                self.rich_log.write(eval(cmd, {}, {}))
            except:
                if cmd and event.input.id == "command-input":
                    try:
                        if "cd " in cmd:
                            cmdpath = cmd.strip("cd ")
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
                                logger.info(f"{cmdpath.is_dir()}")
                                self.notify(message=message, severity="error")

                        elif "cwd" in cmd:
                            self.notify(
                                message=f"{os.getcwd()}",
                                title="Current working directory",
                            )
                        else:
                            self.app.run_worker(
                                self.execute_command(cmd),
                                name="cmd_worker",
                                description=f"Executing: {cmd}",
                            )
                    except Exception as e:
                        self.rich_log.write(f"[error] {str(e)}")
            self.HISTORY.append(cmd)
            save_history(self.HISTORY)
            self.query_one("#directory-tree").refresh()
            self.HISTORY_index = len(self.HISTORY)
            event.input.value = ""

        except PermissionError as e:
            self.rich_log.write(f"error {str(e)}")
            logger.error(
                f"{e} Function: {self.on_input_submitted.__name__} in {Path(__file__).name}"
            )

    async def execute_command(self, cmd: str):
        self.bgrocess_table = self.query_one(DataTable)

        try:
            self.executable = asyncio.create_task(CLI(cmd))
            self.added_process = self.bgrocess_table.add_row(
                id(self.executable), cmd, "[red]cancel"
            )

            result = await self.executable
            logger.info(str(self.added_process))
            if not isinstance(result, Panel):
                self.rich_log.write(Panel(result, expand=False))
            else:
                self.rich_log.write(result)
            self.bgrocess_table.remove_row(self.added_process)
        except ErrorNotify as e:
            self.notify(message=e.message, title="Error", severity="error")
            self.bgrocess_table.remove_row(self.added_process)
        except WarningNotify as e:
            self.notify(message=e.message, title="Warning", severity="warning")
            self.bgrocess_table.remove_row(self.added_process)
        except InfoNotify as e:
            self.notify(message=e.message, title="Information", severity="information")
            self.bgrocess_table.remove_row(self.added_process)

        except Exception as e:
            logger.error(
                f"{e} Function: {self.execute_command.__name__} in {Path(__file__).name}"
            )
            self.rich_log.write(f"[error] Command execution failed: {str(e)}")
            self.bgrocess_table.remove_row(self.added_process)

    def action_toggle_sidebar(self):
        self.sidebar.toggle_class("-hidden")

    async def change_directory(self, cmdpath: Path):
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
            logger.error(
                f"{e} Function: {self.change_directory.__name__} in {Path(__file__).name}"
            )
            self.rich_log.write(f"error Error changing directory: {e}")

    def on_click(self, event: Click):
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

    async def on_worker_failed(self, event):
        """Handle worker failures."""
        self.rich_log.write(f"[error] Worker failed: {event}")

    def is_text_file(self, file_path: str | Path | os.PathLike, block_size=512) -> bool:
        """detects the file is text based or not"""
        try:
            with open(file_path, "rb") as file:
                chunk = file.read(block_size)

                if b"\x00" in chunk:
                    print("in chunk")
                    return False

                try:
                    chunk.decode("utf-8")
                except UnicodeDecodeError:
                    return False

                return True
        except Exception:
            return False

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
