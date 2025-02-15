import os
import asyncio
from pathlib import Path

from rich.panel import Panel
from textual import work
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
from Meine.widgets.input import MeineInput
from Meine.widgets.TextArea import TextEditor


class HomeScreen(Screen[None]):

    AUTO_FOCUS = "#command-input"

    CSS_PATH = Path(__file__).parent.parent / "tcss/app.css"

    HISTORY = load_history()
    HISTORY_INDEX = len(HISTORY)

    BINDINGS = [
        Binding("ctrl+d", "toggle_sidebar", show=False, priority=True),
    ]

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.si = {}
        self.previous_file = None

    def compose(self):
        self.inputconsole = MeineInput(
            placeholder="Enter command....",
            id="command-input",
            history=self.HISTORY,
            history_index=self.HISTORY_INDEX,
        )
        self.rich_log = RichLog(id="output")
        self.sidebar = Directory_tree_container(classes="-hidden")
        self.Dtree = self.sidebar.dtree
        self.bgprocess = Background_process_container(classes="-hidden")
        self.text_area = TextEditor.code_editor(
            id="text_editor",
            language="bash",
            theme=self.app.SETTINGS["text_editor_theme"],
        )
        self.IO_container = Container(self.rich_log, self.inputconsole, id="IO")

        yield Container(
            self.IO_container, self.text_area, self.sidebar, self.bgprocess, id="main"
        )

    def key_ctrl_b(self):
        self.bgprocess.toggle_class("-hidden")



    @work()
    async def show_textarea(self) -> None:
        self.IO_container.add_class("-hidden")
        self.text_area.add_class("-show")

    @work()
    async def hide_textarea(self) -> None:
        self.IO_container.remove_class("-hidden")
        self.text_area.remove_class("-show")

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
            self.query_one("#dt").refresh()
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
        self.query_one(Directory_tree_container).toggle_class("-hidden")

    async def change_directory(self, cmdpath: Path):
        try:
            dtree = self.query_one("#dt", DirectoryTree)
            dtree.path = cmdpath.resolve()
            os.chdir(cmdpath)
            self.si = {}
            # self.rich_log.write(f"Changed directory to {os.getcwd()}")
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
            if event.widget.id == "dt" and event.ctrl:
                self.handle_files_click_input(event.widget)
            elif event.widget.id == "dt":
                tree = self.query_one("#dt", DirectoryTree)
                selected_node = tree.cursor_node.data.path
                if selected_node.is_dir():
                    tree.path = selected_node
                    os.chdir(tree.path)
                elif (selected_node.is_file()):
                    self.notify(f"selected node = {selected_node} ")
                    self.run_worker(self.open_text_editor(selected_node),group="file-open",exclusive=True)



                else:
                    None

        except PermissionError:
            self.notify(title="Error", message="Permission Denied", severity="error")
        except:
            None

    async def on_worker_failed(self, event):
        """Handle worker failures."""
        self.rich_log.write(f"[error] Worker failed: {event}")

    async def open_text_editor(self, path: Path):
        try:
            self.selected_file_path = path
            if not self.is_text_file(self.selected_file_path):
                raise ErrorNotify("unsupported file format")


            if self.previous_file is None  or self.previous_file != path :
                self.show_textarea()
                self.text_area.filepath = self.selected_file_path
                self.previous_file = path
                self.run_worker(self.text_area.read_file(), exclusive=True)
            elif self.previous_file == path:
                self.hide_textarea()
                self.previous_file = None
            else :
                self.notify(f"""
                    selected file = {self.selected_file_path}

""")
        except Exception as e:
            self.notify(f"Unsupported file format {e}")

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
