from textual.widgets import DirectoryTree
from textual.binding import Binding
from pathlib import Path
import os
from Meine.utils.file_loaders import load_settings
import json,csv
from Meine.exceptions import ErrorNotify
from textual import work


class DTree(DirectoryTree):


    

    CLICK_CHAIN_TIME_THRESHOLD = 0.5
    auto_expand = False
    
    BINDINGS = [Binding('left','cd_parent_directory'),Binding('home','cd_home_directory',priority=True),
                Binding('right','select_focused_directory')]
    

    def __init__(self, path, *, name = None, id = None, classes = None, disabled = False):
        super().__init__(path, name=name, id=id, classes=classes, disabled=disabled)
        self.previous_file = None
    
    def filter_paths(self, paths):

        self.show_hidden = load_settings()["show_hidden_files"]
        if (self.show_hidden):
            return paths
        else :
            return [path for path in paths if not path.name.startswith('.')]

    
    def on_directory_tree_directory_selected(self,event:DirectoryTree.DirectorySelected):
        self.auto_expand = False
        if (event.node.is_root):
            self.path = event.path.parent

    async def on_directory_tree_file_selected(self,event:DirectoryTree.FileSelected):
        try:
            self.loading = True
            self.filepath = event.path
            loaded_text = self.read_file()
            loaded_text = await loaded_text.wait()
            
            if (loaded_text):
                if (self.previous_file is None or self.previous_file != event.path):
                    self.screen.show_textarea()
                    self.screen.text_area.text = loaded_text
                    self.screen.text_area.filepath = event.path
                    
                    self.previous_file = event.path
                elif (self.previous_file == event.path):
                    self.screen.hide_textarea()
                    self.previous_file = None
            else:
                self.notify('Unsupported file format')
        except :
            self.notify('Unsupported file format')
        finally:
            self.loading = False
            

    def action_cd_home_directory(self):
        self.path = Path.home()
        os.chdir(self.path)
        self.refresh()

    def action_select_focused_directory(self):
        try:
            focused_path = self.cursor_node.data.path
            if (focused_path and focused_path.is_dir()):
                self.path = focused_path
                os.chdir(self.path)
                self.refresh()
            elif (focused_path.is_file()):
                self.app.notify(f"{focused_path.name} is a file",severity='information')
            else :
                self.app.notify(f"select a folder",severity='warning')
        except PermissionError :
            self.app.notify(f'{focused_path.name} Permission Denied',severity='warning')
    
    def action_cd_parent_directory(self):
        current_path = Path(self.path)
        self.path = current_path.resolve().parent
        os.chdir(self.path)
        self.refresh()



    @work(exclusive=True)
    async def read_file(self) -> str:
        try:
            extension = self.filepath.suffix
            if (extension == 'csv'):
                return self.read_csv_files(self.filepath)
            elif (extension == 'json'):
                return self.read_json_files(self.filepath)
            else :
                return self.read_txt_files(self.filepath)
        except :
            return None
            
    def read_csv_files(self, filepath: Path) -> str:
        try:
            with open(filepath,'r') as file:
                reader = csv.reader(file)
                return '\n'.join([','.join(row) for row in reader])
        except Exception as e:
            self.notify(f'Error in reading csv file {e}')
            raise

    def read_txt_files(self, filepath: str) -> str:
        try:
            with open(filepath,'r') as file:
                return file.read()
        except Exception as e:
            self.notify(f'Error in reading json file  {e}')
            return None

    def read_json_files(self, filepath: Path) -> str:

        try:
            with open(filepath,'r') as file:
                data = json.load(file)
                return json.dumps(data,indent=4)
        except json.JSONDecodeError:
            raise ErrorNotify("Error in reading the file")
        except Exception as e:
            self.notify(f'Error in reading json file  {e}')
