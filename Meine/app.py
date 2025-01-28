import os
import asyncio
from textual.widgets import RichLog,DirectoryTree,DataTable,Input
from textual.app import App,SystemCommand
from rich.panel import Panel
from pathlib import Path
from textual.containers import Container
from textual.events import Click
from textual.binding import Binding
from textual.worker import WorkerFailed
from textual.command import Provider,Hits,Hit
from functools import partial

from Meine.logger_config import logger
from Meine.exceptions import RaiseNotify
from Meine.Screens.settings import Settings,NameGetterScreen
from Meine.Screens.help import HelpScreen

from Meine.utils.file_loaders import load_history
from Meine.utils.file_editor import save_history
from Meine.widgets.input import MeineInput
from Meine.utils.file_editor import add_custom_path_expansion
from Meine.widgets.containers import Directory_tree_container,Background_process_container
from Meine.main import CLI

class CustomCommand(Provider):

    async def search(self,query: str) -> Hits:

        C = 'add custom path expansions'
        matcher = self.matcher(query)

        score = matcher.match(C)
        if (score > 0):
            yield Hit(
                score,
                matcher.highlight(query),
                partial(self.app.push_screen,NameGetterScreen(title=f'{C}',callback=add_custom_path_expansion)),
                help=f'{C}'
            )
        



class MeineAI(App[None]):

    COMMANDS = App.COMMANDS | {CustomCommand}
    def get_system_commands(self, screen):
        yield from super().get_system_commands(screen)
        yield SystemCommand("Settings","open settings",self.key_ctrl_s)
        yield SystemCommand("Help","open the help screen",self.key_ctrl_k)
        yield SystemCommand("add custom path",'add path exp',partial(self.push_NameGetter_screen,'something',add_custom_path_expansion))
    

    CSS_PATH = Path(__file__).parent / "tcss/app.css"
    AUTO_FOCUS = '#input'
    BINDINGS = [
                Binding('ctrl+d','toggle_sidebar',show=False,priority=True),
                ]
    
    RUNNING_TASKS: dict[int] = {}

    def push_NameGetter_screen(self, title, callback):
        self.push_screen(NameGetterScreen(title,callback))
    
    def __init__(self):
        super().__init__()
        self.history = load_history()
        self.history_index = len(self.history)
        self.si = {}
        super().__init__()
        # self.call_later(self.execute_command)

    def compose(self):
        self.inputconsole = MeineInput(placeholder='Enter command....', id="input")
        self.rich_log = RichLog(id="output")
        self.sidebar = Directory_tree_container(classes="-hidden")
        self.bgprocess = Background_process_container(classes='-hidden')

        yield Container(
            Container(self.rich_log, self.inputconsole, id='io'),
            self.sidebar,
            self.bgprocess,
            id="main"
        )
            
    def key_ctrl_k(self):
        try:
            if (self.screen_stack[-1] == 'help_screen'):
                self.pop_screen()
            else :
                self.push_screen(HelpScreen(id='help_screen'))
                self.notify('help')
        except:
            None

    def action_focus_dt(self):
        self.dt = self.query_one('#dt',DirectoryTree)
        if (not self.dt.is_disabled):
            self.dt.focus()
        else :
            None  


    def key_ctrl_s(self):
        try:
            if (self.screen_stack[-1].id == 'setting'):
                self.pop_screen()
            else :
                self.push_screen(Settings(id='setting'))
                self.notify('settings',timeout=2.5)
        except Exception as e:
            logger.error(f'{e} Function: {self.key_ctrl_s.__name__} in {Path(__file__).name}')
            None

    def key_escape(self):
        try:
            self.pop_screen()
        except Exception as e:
            logger.error(f'{e} Function: {self.key_escape.__name__} in {Path(__file__).name}')

    def action_toggle_sidebar(self):
        self.query_one(Directory_tree_container).toggle_class("-hidden")
    



    def key_ctrl_b(self):
        self.bgprocess.toggle_class("-hidden")

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


    def handle_files_click_input(self, widget):

        def qoutes_for_spaced_name(name:str):
            return f"'{name}'" if (' ' in name) else name
        try:
            Dtree = self.query_one('#dt', DirectoryTree)
            selected_node = Dtree.cursor_node.data.path
            name = qoutes_for_spaced_name(selected_node.name)
            input_text = self.inputconsole.value 

            if (not self.si and name not in input_text): #add name
                self.inputconsole.value = f'{input_text.strip()} {name}'
                self.si[name] = selected_node
            elif (name in self.si and name not in input_text):
                if (len(self.si) == 1):
                    self.inputconsole.value = f"{input_text} {name}"
                else :
                    if (' ' in input_text):
                        self.inputconsole.value = f'{input_text},{name}'
                    else :
                        self.inputconsole.value = f'{input_text} {name}'

            elif (self.si and name not in input_text): #add name
                self.inputconsole.value = f'{input_text.strip()},{name}'
                self.si[name] = selected_node
            elif (not self.si and name in input_text):  # remove name
                ''' if user typed by his own '''
                self.inputconsole.value = input_text.replace(name,'')
            else :
                del self.si[name]
                if (f',{name}' in input_text):
                    self.inputconsole.value = input_text.replace(f",{name}",'')
                else :
                    self.inputconsole.value = input_text.replace(name,'')



        except Exception as e:
            self.rich_log.write(f"error clicks {e}")
            logger.error(f'{e} Function: {self.handle_files_click_input.__name__} in {Path(__file__).name}')

        


    def on_click(self, event: Click):
        try:
            if event.widget.id == 'dt' and event.ctrl :
                self.handle_files_click_input(event.widget)
            elif event.widget.id == 'dt' :
                tree = self.query_one('#dt', DirectoryTree)
                selected_node = tree.cursor_node
                if selected_node.data.path.is_dir():
                    tree.path = selected_node.data.path
                    os.chdir(tree.path)
                    self.si = {}
                else:
                    None                
            elif event.widget.id == 'setting':
                self.pop_screen()
            else :
                None
        except PermissionError:
            self.notify(title='Error',message='Permission Denied',severity='error')
        except Exception as e:
            logger.error(f'{e} Function: {self.on_click.__name__} in {Path(__file__).name}')
            self.notify(str(e))
        logger.info(f'{event.widget.id} {event.screen_offset}')
            

    async def on_input_submitted(self, event: Input.Submitted):
        if (self.screen == '#_default'):
            try:
                async def safe_eval(cmd,allow_function):
                    
                    result = eval(cmd,allow_function,{})
                    self.query_one(RichLog).write(result)
                console = self.query_one('#output')
                cmd = event.value.strip()
                try:
                    console.write(eval(cmd,{},{}))
                except:
                    if cmd:
                        try:
                            if 'cd ' in cmd:
                                cmdpath = cmd.strip('cd ')
                                cmdpath = Path(cmdpath)
                                if (cmdpath.is_dir()):
                                    self.run_worker(self.app.change_directory(cmdpath), name="cd_worker", description="Change Directory")
                                    self.notify(message=f'{str(cmdpath.resolve())}',title="changed directory")
                
                                else:
                                    message = f'{cmdpath} is file' if cmdpath.is_file() else f'{cmdpath} Not Found' 
                                    logger.info(f'{cmdpath.is_dir()}')
                                    self.notify(message=message,severity="error")
                                
                            elif 'cwd' in cmd:
                                self.notify(message=f"{os.getcwd()}",title="Current working directory")
                            else:
                                self.run_worker(self.execute_command(cmd), name="cmd_worker", description=f"Executing: {cmd}")
                        except Exception as e:
                            console.write(f"[error] {str(e)}")
                self.history.append(cmd)
                save_history(self.history)
                self.query_one("#dt").refresh()
                self.history_index = len(self.history)
                event.input.value = ''

            except PermissionError as e:
                console.write(f"error {str(e)}")
                logger.error(f'{e} Function: {self.on_input_submitted.__name__} in {Path(__file__).name}')



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
            logger.error(f'{e} Function: {self.change_directory.__name__} in {Path(__file__).name}')
            self.rich_log.write(f"error Error changing directory: {e}")
            

    async def execute_command(self, cmd: str):
        self.bgrocess_table = self.query_one(DataTable)

        try:
            self.executable = asyncio.create_task(CLI(cmd))
            self.added_process = self.bgrocess_table.add_row(id(self.executable),cmd,'[red]cancel')

            result = await self.executable
            logger.info(str(self.added_process))
            if (not isinstance(result,Panel)):
                self.rich_log.write(Panel(result,expand=False))
            else :
                self.rich_log.write(result)
            self.bgrocess_table.remove_row(self.added_process)
        except RaiseNotify as e:
            self.notify(message=e.message,title='Error',severity='error')
            self.bgrocess_table.remove_row(self.added_process)

        except Exception as e:
            logger.error(f'{e} Function: {self.execute_command.__name__} in {Path(__file__).name}')
            self.rich_log.write(f"[error] Command execution failed: {str(e)}")
            self.bgrocess_table.remove_row(self.added_process)
        


    async def on_worker_failed(self, event: WorkerFailed):
        """Handle worker failures."""
        self.rich_log.write(f"[error] Worker failed: {event}")


def run():
    MeineAI().run()