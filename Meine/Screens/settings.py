from pathlib import Path

from textual.widgets import Static,Switch,Button ,Input,Select
from textual.containers import Container,Horizontal
from textual.events import Click
from textual.screen import ModalScreen

from Meine.utils.file_loaders import load_settings
from Meine.utils.file_editor import save_settings,clear_history
from Meine.Screens.me import Myself


class Settings(ModalScreen):

    def __init__(self, name = None, id = None, classes = None):
        self.text_area = self.app.query_one('#text_editor')
        super().__init__(name, id, classes)


    CSS_PATH = Path(__file__).parent.parent / 'tcss/setting.css'


    AVAILABLE_THEMES = {
            'dracula', 'github_light', 'monokai',
            'vscode_dark', 'css'
            }

    AVAILABLE_LANGUAGES = {
            'json', 'markdown', 'go',   
            'javascript', 'yaml', 'regex',
            'bash', 'rust', 'toml', 
            'python', 'css', 'html', 
            'java', 'xml', 'sql'
        }

    def compose(self):
        self.setting_json = load_settings()

        self.select_text_editor_theme = Select(
            [(themes,themes) for themes in self.AVAILABLE_THEMES],
            prompt='choose a theme',allow_blank=False,
            id='select-text-editor-theme'
            )
        
        self.select_app_theme = Select(
            [(themes,themes) for themes in self.app._registered_themes.keys()],
            prompt='choose a theme',allow_blank=False,
            id='select-app-theme'
            )
        self.select_text_editor_language = Select(
            [(lang,lang) for lang in self.AVAILABLE_LANGUAGES],
            prompt='choose a language',allow_blank=False,
            id='select-text-editor-language')

        yield Container(
            Static('settings',id='settings-title'),
            
                Horizontal(Static('show hidden files',classes='caption'),Switch(id='hidden_files_sw',value=self.setting_json['show_hidden_files'])),
                Horizontal(Static('clear history',classes='caption'),Button(label='clear',id='clear_history_bt')),
                Horizontal(Static('text app theme',classes='caption'),self.select_app_theme),
                Horizontal(Static('text editor theme',classes='caption'),self.select_text_editor_theme),
                Horizontal(Static('text editor language',classes='caption'),self.select_text_editor_language),
            
            Button(label='About me',variant='success',id='about_me_bt')
        )


    
    def on_click(self, event:Click):
        if (str(event.widget.id) == 'settings-screen'):
            self.dismiss()
        

    def on_button_pressed(self,event:Button.Pressed):
        if (event.button.id == 'about_me_bt'):
            self.dismiss()
            self.app.push_screen(Myself())
        if (event.button.id == 'clear_history_bt'):
            clear_history()
            self.notify(f'Command history is cleared ,restart required (optional)!')
            
    

    
    def on_switch_changed(self, event:Switch.Changed):
            if (event.switch.id == 'hidden_files_sw'):
                self.setting_json['show_hidden_files'] = event.value
            save_settings(self.setting_json)

    def _on_mount(self):
        self.select_text_editor_language.value = self.text_area.language
        self.select_text_editor_theme.value = self.text_area.theme
        self.select_app_theme.value = self.app.theme


    def on_select_changed(self, event: Select.Changed):
        if (event.select.id == 'select-text-editor-theme'):
            self.text_area.theme = event.value
            self.app.SETTINGS['text_editor_theme'] = event.value
        elif (event.select.id == 'select-text-editor-language'):
            self.text_area.language = event.value
        elif (event.select.id == 'select-app-theme'):
            self.app.theme = event.value
            self.app.SETTINGS['app_theme'] = event.value
        save_settings(self.app.SETTINGS)

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



