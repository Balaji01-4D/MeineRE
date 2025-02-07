from textual.widgets import TextArea
from textual import work
from pathlib import Path
import json,csv
from textual.worker import Worker


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

    def __init__(self, text = "", *, language = None, theme = "css", soft_wrap = True, tab_behavior = "focus", read_only = False, show_line_numbers = False, line_number_start = 1, max_checkpoints = 50, name = None, id = None, classes = None, disabled = False, tooltip = None):
        super().__init__(text, language=language, theme=theme, soft_wrap=soft_wrap, tab_behavior=tab_behavior, read_only=read_only, show_line_numbers=show_line_numbers, line_number_start=line_number_start, max_checkpoints=max_checkpoints, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip)
        self.filepath = None
            


    @work(thread=True)
    async def key_ctrl_s(self):
        with open(self.filepath,'w') as file:
            file.writelines(self.text)
        self.notify(f'{self.filepath.name} saved successfully')
    

    @work(thread=True,name='read-file')
    async def read_file(self) -> str:
        try:
            extension = self.filepath.suffix
            if (extension == 'csv'):
                text = await self.read_csv_files(self.filepath).wait()
                return (text,'json')
            elif (extension == 'json'):
                text = await self.read_json_files(self.filepath).wait()
                return (text,'json')
            else :
                text = self.read_txt_files(self.filepath)
                syntax = await self.get_syntax_highlighting(extension)
                return (text,syntax)
        except :
            return None
            
    async def get_syntax_highlighting(self,extension):

        if (extension in SYNTAX_HIGHLIGHTING_SUPPORTED_FILES):
            return SYNTAX_HIGHLIGHTING_SUPPORTED_FILES[extension]
        elif (extension in PROGRAMMING_AND_SCRIPTING_LANGUAGES):
            return 'bash'
        elif (extension in CONFIG_AND_DATA_FILES):
            return 'json'
        else:
            return 'markdown'
        
    @work()
    async def read_csv_files(self, filepath: Path) -> str:
        try:
            with open(filepath,'r') as file:
                reader = csv.reader(file)
                return '\n'.join([','.join(row) for row in reader])
        except Exception :
            return None

    @work()
    async def read_txt_files(self, filepath: str) -> str:
        try:
            with open(filepath,'r') as file:
                return file.read()
        except Exception :
            return None

    @work(thread=True)
    async def read_json_files(self, filepath: Path) -> str:
        try:
            with open(filepath,'r') as file:
                data = json.load(file)
                return json.dumps(data,indent=4)
        except Exception:
            return None


    def on_worker_state_changed(self, event:Worker.StateChanged):
        if (event.worker.name == 'read-file' and event.worker.is_finished):
            self.text = event.worker.result


