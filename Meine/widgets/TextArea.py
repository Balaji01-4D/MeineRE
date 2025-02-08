from textual.widgets import TextArea
from textual import work
from pathlib import Path
import json,csv
from textual.worker import Worker
from textual.events import Key
from textual.binding import Binding
from Meine.logger_config import logger




SYNTAX_HIGHLIGHTING_SUPPORTED_FILES = {
    '.py':'python','.java':'java','.css':'css','.html':'html','.json':'json'
    ,'.rs':'rust','.go':'go','.sql':'sql','.xml':'xml','.toml':'toml','.md':'markdown'
    ,'.yaml':'yaml','.markdown':'markdown','.htm':'html','.sh':'bash','.yml':'yaml'
    }

PROGRAMMING_AND_SCRIPTING_LANGUAGES = {
    '.c','.cpp','.cs','.kt',
    '.kts','.pl','swift','.php',
    '.rb','.ts','.bat','.cmd','.ps1'
}

CONFIG_AND_DATA_FILES = {
    '.csv','.tsv','.ini','.env','.conf','.gitconfig'
}

DOCUMENTATION_AND_MIXED_CONTENT_FILES = {
    '.rst','.tex','.adoc','.log','.txt'
}

class TextEditor(TextArea):
    
    BRACKET_PAIRS = {
        '{':'}','[':']',
        '(':')','"':'"',
        "'":"'"
    }

    BINDINGS = [
        Binding("ctrl+shift+up",'open_settings','open settings',priority=True)
    ]

    def __init__(self, text = "", *, language = None, theme = "css", soft_wrap = True, tab_behavior = "focus", read_only = False, show_line_numbers = False, line_number_start = 1, max_checkpoints = 50, name = None, id = None, classes = None, disabled = False, tooltip = None):
        super().__init__(text, language=language, theme=theme, soft_wrap=soft_wrap, tab_behavior=tab_behavior, read_only=read_only, show_line_numbers=show_line_numbers, line_number_start=line_number_start, max_checkpoints=max_checkpoints, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip)
        self.filepath: Path|None = None
            

    def action_open_settings(self):
        self.notify("opened settings")

    @work(thread=True)
    async def key_ctrl_s(self):
        with open(self.filepath,'w') as file:
            file.writelines(self.text)
        self.notify(f'{self.filepath.name} saved successfully')

        
    
    
    async def read_file(self) -> None:
        try:
            self.loading = True
            extension = self.filepath.suffix
            self.get_syntax_highlighting(extension)
            if (extension == 'csv'):
                self.run_worker(self.read_csv_files(self.filepath))
            elif (extension == 'json'):
                self.run_worker(self.read_json_files(self.filepath))
            else :
                self.run_worker(self.read_txt_files(self.filepath))
            
        except Exception as e:
            self.notify(f'{e}')

    def _on_key(self, event: Key):
        if (event.character in self.BRACKET_PAIRS):
            self.insert(f"{event.character}{self.BRACKET_PAIRS[event.character]}")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()
        
    

    @work(thread=True)
    def get_syntax_highlighting(self, extension: str) -> None:
        ''' sets a syntax highlighting based on the file extension & category '''
        if (extension in SYNTAX_HIGHLIGHTING_SUPPORTED_FILES):
            self.language = SYNTAX_HIGHLIGHTING_SUPPORTED_FILES[extension]
        elif (extension in PROGRAMMING_AND_SCRIPTING_LANGUAGES):
            self.language = 'bash'
        elif (extension in CONFIG_AND_DATA_FILES):
            self.language = 'json'
        else:
            self.language = 'markdown'
        
    
    async def read_csv_files(self, filepath: Path) -> None:
        try:
            with open(filepath,'r') as file:
                reader = csv.reader(file)
                self.text = '\n'.join([','.join(row) for row in reader])
        except Exception :
            self.text = ""
            self.notify("unsupported file format")

    async def read_txt_files(self, filepath: str) -> str:
        try:
            with open(filepath,'r') as file:
                self.text = file.read()
        except Exception :
            self.text = ""
            self.notify("unsupported file format")

    async def read_json_files(self, filepath: Path) -> str:
        try:
            with open(filepath,'r') as file:
                data = json.load(file)
                return json.dumps(data,indent=4)
        except Exception:
            self.text = ""
            self.notify("unsupported file format")

    def on_worker_state_changed(self, event:Worker.StateChanged):
        if (event.worker.is_finished):
            self.loading = False





