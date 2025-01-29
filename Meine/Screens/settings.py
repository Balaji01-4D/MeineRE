from pathlib import Path

from textual.widgets import Static,Switch,Button ,Input
from textual.containers import Container,Vertical,Horizontal
from textual.events import Click
from textual.screen import ModalScreen


from Meine.utils.file_loaders import load_settings
from Meine.utils.file_editor import save_settings
from Meine.Screens.me import Myself


class Settings(ModalScreen):

    CSS_PATH = Path(__file__).parent.parent / 'tcss/setting.css'


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
    

class NameGetterScreen(ModalScreen):
     
    CSS_PATH = Path(__file__).parent.parent / 'tcss/setting.css'

    def __init__(self, title , callback , name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.callback = callback
        self.title = title

    def compose(self):
        with Container():
            yield Static(self.title,id='title')
            yield Input(id='Input_of_utils')

    def on_input_submitted(self, event: Input.Submitted):
        self.app.pop_screen()
        result = self.callback(event.value)
        self.app.notify(result)
