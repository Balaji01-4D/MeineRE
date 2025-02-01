from textual.widgets import TextArea
from textual import work
from pathlib import Path
import json
import csv
from Meine.exceptions import ErrorNotify
from Meine.logger_config import logger
import mimetypes

class TextEditor(TextArea):

    def __init__(self, text = "", *, language = None, theme = "css", soft_wrap = True, tab_behavior = "focus", read_only = False, show_line_numbers = False, line_number_start = 1, max_checkpoints = 50, name = None, id = None, classes = None, disabled = False, tooltip = None):
        super().__init__(text, language=language, theme=theme, soft_wrap=soft_wrap, tab_behavior=tab_behavior, read_only=read_only, show_line_numbers=show_line_numbers, line_number_start=line_number_start, max_checkpoints=max_checkpoints, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip)
        self.filepath = None
            
    async def load_file(self,filepath: Path):
        self.notify('load file is called')
        self.loading = True
        self.filepath = filepath
        loaded_text = self.read_file()
        loaded_text = await loaded_text.wait()
        
        if (not loaded_text):
            self.notify('unsupported file format')
            return
        
        elif (filepath and loaded_text):
            self.text = loaded_text
            self.notify('text updated')
        self.loading = False

    @work(exclusive=True)
    async def key_ctrl_s(self):
        with open(self.filepath,'w') as file:
            file.writelines(self.text)
        self.notify(f'{self.filepath.name} saved successfully')


    @work(exclusive=True)
    async def read_file(self) -> str:
        extension = self.filepath.suffix
        if (extension == 'csv'):
            return self.read_csv_files(self.filepath)
        elif (extension == 'json'):
            return self.read_json_files(self.filepath)
        else :
            return self.read_txt_files(self.filepath)
        
    def read_csv_files(self, filepath: Path) -> str:
        try:
            with open(filepath,'r') as file:
                reader = csv.reader(file)
                return '\n'.join([','.join(row) for row in reader])
        except Exception as e:
            self.notify(f'Error in reading csv file {e}')


    def read_txt_files(self, filepath: str) -> str:
        self.notify(f'read text files is called')
        try:
            with open(filepath,'r') as file:
                return file.read()
        except Exception as e:
            self.notify(f'Error in reading a file {e}')

    def read_json_files(self, filepath: Path) -> str:
        self.notify(f'read json files is called')

        try:
            with open(filepath,'r') as file:
                data = json.load(file)
                return json.dumps(data,indent=4)
        except json.JSONDecodeError:
            raise ErrorNotify("Error in reading the file")
        except Exception as e:
            self.notify(f'Error in reading json file  {e}')



            

    

                

    

    @work(exclusive=True)
    async def is_text_file(self, filepath: Path) -> bool:
        
        mime_type,_ = mimetypes.guess_type(filepath)
        return mime_type is not None and mime_type.startswith('text/')



    @work(exclusive=True)
    async def is_binary_file(self, filepath: Path) -> bool:
        try:
            with open(filepath,'rb') as file:
                chunk = file.read(1024)
                if b"\x00" in chunk:
                    return True
        except Exception :
            return True
        return False