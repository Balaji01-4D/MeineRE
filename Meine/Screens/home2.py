import os
import asyncio
from pathlib import Path
from collections import deque
from rich.panel import Panel
from textual.screen import Screen
from textual.widgets import RichLog, Input, DataTable, DirectoryTree, TextArea
from textual.binding import Binding
from textual.events import Click

from Meine.exceptions import InfoNotify, ErrorNotify, WarningNotify
from Meine.widgets.containers import Directory_tree_container, Container, Background_process_container
from Meine.widgets.input import MeineInput
from Meine.logger_config import logger
from Meine.utils.file_loaders import load_history
from Meine.utils.file_editor import save_history
from Meine.main import CLI

class HomeScreen(Screen[None]):
    AUTO_FOCUS = '#input'
    CSS_PATH = Path(__file__).parent.parent / "tcss/app.css"
    
    BINDINGS = [
        Binding('ctrl+d', 'toggle_sidebar', show=False, priority=True),
    ]

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.HISTORY = deque(load_history(), maxlen=100)
        self.HISTORY_INDEX = len(self.HISTORY)
        self.si = {}
        self._task_semaphore = asyncio.Semaphore(10)
        self._bg_process_table = None
        self._directory_tree = None

    @property
    def directory_tree(self) -> DirectoryTree:
        if not self._directory_tree:
            self._directory_tree = self.query_one("#dt", DirectoryTree)
        return self._directory_tree

    @property
    def bg_process_table(self) -> DataTable:
        if not self._bg_process_table:
            self._bg_process_table = self.query_one(DataTable)
        return self._bg_process_table

    def compose(self):
        self.inputconsole = MeineInput(
            placeholder='Enter command....', 
            id="input",
            history=list(self.HISTORY),
            history_index=self.HISTORY_INDEX
        )
        self.rich_log = RichLog(id="output")
        self.sidebar = Directory_tree_container(classes="-hidden")
        self.bgprocess = Background_process_container(classes='-hidden')
        self.text_area = TextArea(id='textarea')

        yield Container(
            Container(self.rich_log, self.inputconsole, id='IO'),
            self.text_area,
            self.sidebar,
            self.bgprocess,
            id="main"
        )

    def key_ctrl_b(self):
        self.bgprocess.toggle_class("-hidden")

    def replace_IO_TextArea(self) -> TextArea:
        self.query_one('#IO', Container).toggle_class("-hidden")
        self.query_one('#textarea', TextArea).toggle_class('-show')
        return self.text_area

    def _quote_name_if_spaced(self, name: str) -> str:
        return f"'{name}'" if ' ' in name else name

    def _add_name_to_input(self, name: str, input_text: str) -> str:
        if not input_text.strip():
            return name
        return f"{input_text.strip()}, {name}" if ',' in input_text else f"{input_text.strip()} {name}"

    def _remove_name_from_input(self, name: str, input_text: str) -> str:
        return input_text.replace(f", {name}", '').replace(name, '').strip()

    def handle_files_click_input(self, widget):
        try:
            selected_node = self.directory_tree.cursor_node.data.path
            name = self._quote_name_if_spaced(selected_node.name)
            input_text = self.inputconsole.value

            if name in input_text:
                new_value = self._remove_name_from_input(name, input_text)
                if name in self.si:
                    del self.si[name]
            else:
                new_value = self._add_name_to_input(name, input_text)
                self.si[name] = selected_node

            self.inputconsole.value = new_value

        except Exception as e:
            logger.error(f'{e} in {self.handle_files_click_input.__name__}')
            self.rich_log.write(f"[error] Click handling failed: {str(e)}")

    async def on_input_submitted(self, event: Input.Submitted):
        try:
            cmd = event.value.strip()
            if not cmd:
                return

            if cmd.startswith('cd '):
                await self.handle_cd_command(cmd)
            elif cmd == 'cwd':
                self.notify(f"Current directory: {os.getcwd()}", title="CWD")
            else:
                self.app.run_worker(
                    self.execute_command(cmd),
                    name="cmd_worker",
                    description=f"Executing: {cmd}"
                )

            self.HISTORY.append(cmd)
            asyncio.create_task(self.save_history_async())
            event.input.value = ''

        except Exception as e:
            logger.error(f"Input error: {e}")
            self.rich_log.write(f"[error] {str(e)}")

    async def handle_cd_command(self, cmd: str):
        try:
            cmdpath = Path(cmd[3:].strip()).expanduser()
            if not cmdpath.exists():
                raise FileNotFoundError(f"Path not found: {cmdpath}")
                
            await self.change_directory(cmdpath)
            self.notify(f"Changed to: {cmdpath.resolve()}", title="Directory Changed")
            
        except Exception as e:
            self.rich_log.write(f"[error] CD failed: {str(e)}")
            logger.error(f"CD error: {e}")

    async def execute_command(self, cmd: str):
        async with self._task_semaphore:
            try:
                task_id = id(asyncio.current_task())
                self.bg_process_table.add_row(str(task_id), cmd, '[red]cancel')
                
                result = await CLI(cmd)
                
                if isinstance(result, Panel):
                    self.rich_log.write(result)
                else:
                    self.rich_log.write(Panel(str(result), expand=False))
                    
            except (ErrorNotify, WarningNotify, InfoNotify) as e:
                self.notify(e.message, title=e.__class__.__name__, severity=e.severity)
            except Exception as e:
                logger.error(f"Command failed: {e}")
                self.rich_log.write(f"[error] Execution failed: {str(e)}")
            finally:
                self.bg_process_table.remove_row(str(task_id))

    async def save_history_async(self):
        try:
            await asyncio.to_thread(save_history, list(self.HISTORY))
        except Exception as e:
            logger.error(f"History save failed: {e}")

    async def change_directory(self, cmdpath: Path):
        try:
            os.chdir(cmdpath)
            self.directory_tree.path = cmdpath.resolve()
            self.directory_tree.reload()
            self.si.clear()
        except PermissionError:
            raise PermissionError(f"Access denied: {cmdpath}")
        except Exception as e:
            logger.error(f"Directory change failed: {e}")
            raise

    def on_click(self, event: Click):
        try:
            if event.widget.id == 'dt':
                if event.ctrl:
                    self.handle_files_click_input(event.widget)
                else:
                    selected_node = self.directory_tree.cursor_node
                    if selected_node.data.path.is_dir():
                        asyncio.create_task(self.change_directory(selected_node.data.path))
        except PermissionError as e:
            self.notify(str(e), title="Error", severity="error")
        except Exception as e:
            logger.error(f"Click error: {e}")

    async def on_worker_failed(self, event):
        self.rich_log.write(f"[error] Worker failed: {event.error}")

    def action_toggle_sidebar(self):
        self.sidebar.toggle_class("-hidden")