import os
from re import search
from pathlib import Path
from textual.widgets import Input,RichLog
from textual.suggester import SuggestFromList
from textual.binding import Binding

from Meine.utils.file_loaders import load_history,load_Path_expansion
from Meine.utils.file_editor import save_history,add_custom_path_expansion
from Meine.logger_config import logger
from Meine.Actions.exceptions import RaiseNotify



actions = ['uz','z','zip','del','c','mk','create','make','unzip','delete','copy','cp'
           ,'rename','rn']

class MeineInput(Input):

    ALLOWED_FUNCTION ={
        'addpath':add_custom_path_expansion
    }


    BINDINGS = [
            Binding('up','history_up','navigate the history up',show=False),
            Binding('down','history_down','navigate the history down',show=False)
            ]

    def __init__(self, value = None, placeholder = "", highlighter = None, password = False, *, restrict = None, type = "text", max_length = 0, suggester = SuggestFromList(actions), validators = None, validate_on = None, valid_empty = False, select_on_focus = True, name = None, id = None, classes = None, disabled = False, tooltip = None):
        super().__init__(value, placeholder, highlighter, password, restrict=restrict, type=type, max_length=max_length, suggester=suggester, validators=validators, validate_on=validate_on, valid_empty=valid_empty, select_on_focus=select_on_focus, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip)
        self.history = load_history()
        self.history_index = len(self.history)


    def action_history_up(self):
        if (self.history_index > 0):
            self.history_index -= 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)

    def on_input_changed(self):
        keyWordMatch = search(r'\{(.+)\}',self.value)
        if (keyWordMatch):
            self.path_expansion(keyWordMatch.group(1))
        else :
            None
    
    def path_expansion(self,keyword: str):
        current_dir = Path.cwd()

        DEFAULT_PATH_EXPANSION: dict[str|Path] = {
            'home':Path.home(),
            'current':current_dir,
            '<-' : current_dir.parent,
            'this':current_dir,
            'parent': current_dir.parent,
            'parent+':current_dir.parent.parent,
            'parent++':current_dir.parent.parent.parent
        }


        USERDEFINED_EXPANSION = load_Path_expansion()
        if (keyword in DEFAULT_PATH_EXPANSION):
            ReplaceBy = str(DEFAULT_PATH_EXPANSION[keyword])
            self.value = self.value.replace(f'{{{keyword}}}',ReplaceBy) 
        elif (keyword in USERDEFINED_EXPANSION):
            ReplaceBy = USERDEFINED_EXPANSION[keyword]
            self.value = self.value.replace(f'{{{keyword}}}',ReplaceBy)
        else :
            self.notify(f'{keyword} Is Not Found and It Is Removed For Good.',severity='error',title='Not Found')



    def action_history_down(self):
        try:
            if (self.history_index < len(self.history) -1):
                self.history_index += 1
                self.value = self.history[self.history_index]
                self.cursor_position = len(self.value)

            else:
                self.history_index = len(self.history)
                self.value = ''
        except Exception as e:
            logger.error(f'{e} Function: {self.action_history_down.__name__} in {Path(__file__).name}')
            None

    


    async def on_input_submitted(self, event: Input.Submitted):
        async def safe_eval(cmd,allow_function):
            
            result = eval(cmd,allow_function,{})
            self.app.query_one(RichLog).write(result)
        console = self.app.query_one('#output')
        try:
            cmd = event.value.strip()
            try:
                self.run_worker(safe_eval(cmd,self.ALLOWED_FUNCTION))
            except:
                if cmd:
                    try:
                        if 'cd ' in cmd:
                            cmdpath = cmd.replace('cd ', '')
                            cmdpath = Path(cmdpath)
                            if (cmdpath.is_dir()):
                                self.run_worker(self.app.change_directory(cmdpath), name="cd_worker", description="Change Directory")
                                self.notify(message=f'{str(cmdpath.resolve())}',title="changed directory")
                            else:
                                self.notify(message="It is Not exists",severity="error")
                            
                        elif 'cwd' in cmd:
                            self.notify(message=f"{os.getcwd()}",title="Current working directory")
                        else:
                            self.run_worker(self.app.execute_command(cmd), name="cmd_worker", description=f"Executing: {cmd}")
                    except Exception as e:
                        console.write(f"[error] {str(e)}")
            self.history.append(cmd)
            save_history(self.history)
            self.app.query_one("#dt").refresh()
            self.history_index = len(self.history)
            event.input.value = ''

        except PermissionError as e:
            console.write(f"error {str(e)}")
            logger.error(f'{e} Function: {self.on_input_submitted.__name__} in {Path(__file__).name}')