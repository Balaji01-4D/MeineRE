from textual.widgets import RichLog,Input,DirectoryTree,Static,Switch,Button
from textual.app import App
from rich.panel import Panel
from pathlib import Path
import os
import time
import asyncio
from textual.suggester import SuggestFromList
from textual.containers import Container,Vertical,Horizontal
from textual.events import Click
from textual.binding import Binding
from textual.screen import ModalScreen
import json
from textual.worker import WorkerFailed
from Dtree import DTree
from main import CLI
from MeineAI.Actions import RaiseNotify
from tui.me import Myself
import xdialog
from logger_config import logger
actions = ['uz','z','zip','del','c','mk','create','make','unzip','delete','copy','cp'
           ,'rename','rn']
history_loc = Path(__file__).parent /'tui/history.json' 
settings_loc = Path(__file__).parent /'tui/settings.json'


def load_settings():
    try:
        with open(settings_loc,'r') as setfile:
            data = setfile.read().strip()
            return json.loads(data) 
    except (json.JSONDecodeError,FileNotFoundError):
        None

def load_history():
    try:
        with open(history_loc,'r') as histfile:
            data = histfile.read().strip()
            return json.loads(data) 
    except (json.JSONDecodeError,FileNotFoundError):
        with open(history_loc,'w') as histfile:
            json.dump([],histfile)
        return []

def save_history(history):
    with open(history_loc,'w') as file:
        if (open(history_loc).read() == '[]'):
            json.dump([],file,indent=4)
        json.dump(history,file,indent=4)

def clear_history():
    with open(history_loc,'w') as file:
        json.dump([],file,indent=4)

def save_settings(settings):
    with open(settings_loc,'a') as file:
        json.dump(settings,file,indent=4)


show_hidden_files = False
items = []

     

class MeineAI(App):
    
    theme = 'tokyo-night'

    CSS_PATH = Path(__file__).parent / "tui/final.css"
    AUTO_FOCUS = '#input'
    BINDINGS = [
                Binding('up','history_up','navigate the history up',show=False),
                Binding('down','history_down','navigate the history down',show=False),
                Binding('ctrl+d','toggle_sidebar',show=False,priority=True),
                Binding('ctrl+l','toggle_log',show=False,priority=True),
                ]
    

    def __init__(self):
        super().__init__()
        self.history = load_history()
        self.history_index = len(self.history)
        self.si = {}
        # self.call_later(self.execute_command)


    def compose(self):
        self.inputconsole = Input(placeholder='Enter command....', id="input", suggester=SuggestFromList(actions, case_sensitive=False))
        self.rich_log = RichLog(id="output")
        self.sidebar = DTsideBar(classes="-hidden")

        
        yield Container(
            Container(self.rich_log, self.inputconsole, id='io'),
            self.sidebar,
            id="main"
        )
    
    def key_ctrl_z(self):
        yes = xdialog.directory('select the directory')
        if (yes):
            self.inputconsole.value = yes
            self.query_one(DirectoryTree).path = yes


    def action_history_up(self):
        if (self.history_index > 0):
            self.history_index -= 1
            self.inputconsole.value = self.history[self.history_index]
            self.inputconsole.cursor_position = len(self.inputconsole.value)
            
        
    
    def action_history_down(self):
        try:
            if (self.history_index < len(self.history) -1):
                self.history_index += 1
                self.inputconsole.value = self.history[self.history_index]
                self.inputconsole.cursor_position = len(self.inputconsole.value)

            else:
                self.history_index = len(self.history)
                self.inputconsole.value = ''
        except Exception as e:
            logger.error(f'{e} Function: {self.action_history_down.__name__} in {Path(__file__).name}')
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

            None

    def action_toggle_sidebar(self):
        self.query_one(DTsideBar).toggle_class("-hidden")

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
        except PermissionError:
            self.notify(title='Error',message='Permission Denied',severity='error')
        except Exception as e:
            logger.error(f'{e} Function: {self.on_click.__name__} in {Path(__file__).name}')
            self.notify(str(e))




    async def on_input_submitted(self, event: Input.Submitted):
        console = self.query_one('#output', RichLog)
        try:
            cmd = event.value.strip()
            try:
                self.rich_log.write(eval(cmd))
            except:
                if cmd:
                    try:
                        if 'cd ' in cmd:
                            cmdpath = cmd.replace('cd ', '')
                            cmdpath = Path(cmdpath)
                            if (cmdpath.is_dir()):
                                self.run_worker(self.change_directory(cmdpath), name="cd_worker", description="Change Directory")
                                self.notify(message=f'{str(cmdpath.resolve())}',title="changed directory")
                            else:
                                self.notify(message="It is Not exists",severity="error")
                            
                        elif 'cwd' in cmd:
                            self.notify(message=f"{os.getcwd()}",title="Current working directory")
                        else:
                            self.run_worker(self.execute_command(cmd), name="cmd_worker", description=f"Executing: {cmd}")
                    except Exception as e:
                        console.write(f"[error] {str(e)}")
                    self.history.append(cmd)
                    save_history(self.history)
                    self.query_one("#dt", DirectoryTree).refresh()
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
        start_time = time.time()
        """Worker for executing commands."""
        try:

            notify_task = asyncio.create_task(self.notify_if_delay(start_time))
            result = await CLI(cmd)
            if (not isinstance(result,Panel)):
            
                self.rich_log.write(Panel(result,expand=False))
            else :
                self.rich_log.write(result)
        except RaiseNotify as e:
            self.notify(message=e.message,title='Error',severity='error')
        
        except Exception as e:
            logger.error(f'{e} Function: {self.execute_command.__name__} in {Path(__file__).name}')
            self.rich_log.write(f"[error] Command execution failed: {str(e)}")

    async def notify_if_delay(self,start_time):
        await asyncio.sleep(3)

        elapsed_time = time.time() - start_time

        if (elapsed_time >= 3):
            self.notify("Task is running in the background")


    async def on_worker_failed(self, event: WorkerFailed):
        """Handle worker failures."""
        self.rich_log.write(f"[error] Worker failed: {event}")





class DTsideBar(Container):
    def compose(self):
        dtree = DTree(path='/home/balaji/testings',id='dt')
        self.dtree_log = RichLog(id='dtree_log')
        yield dtree
        os.chdir(dtree.path)

    
class Settings(ModalScreen):

    CSS_PATH = Path(__file__).parent / 'tui/setting.css'


    def compose(self):
        self.setting_json = load_settings()
        yield Container(
            Static('settings',id='label'),
            Vertical(
                Horizontal(Static('[red]show hidden files'),Switch(id='hidden_files_sw',value=self.setting_json['show_hidden_files'])),
                Horizontal(Static('[red]clear history'),Button(label='clear',id='clear_history_bt')),
            ),
            Button(label='About me',variant='success',id='about_me_bt')
        )


    
    def on_click(self, event:Click):
        if (str(event.widget) == str(Settings())):
            self.dismiss()

    def on_button_pressed(self,event:Button.Pressed):
        if (event.button.id == 'about_me_bt'):
            self.dismiss()
            self.app.push_screen(Myself())
        if (event.button.id == 'clear_history_bt'):
            self.app.history = []
            
    

    
    def on_switch_changed(self,event:Switch.Changed):
            if (event.switch.id == 'hidden_files_sw'):
                self.setting_json['show_hidden_files'] = event.value
            save_settings(self.setting_json)
    


if (__name__ == "__main__"):
    MeineAI().run()

