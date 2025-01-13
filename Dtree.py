from textual.widgets import DirectoryTree
from textual.binding import Binding
from pathlib import Path
import json
import os
from textual import on
from logger_config import logger
settings_loc = Path(__file__).parent / 'tui/settings.json'

items =[]

class DTree(DirectoryTree):
    

    CLICK_CHAIN_TIME_THRESHOLD = 0.5
    auto_expand = False
    
    BINDINGS = [Binding('left','cd_parent_directory'),Binding('home','cd_home_directory',priority=True),
                Binding('right','select_focused_directory')]
    def filter_paths(self, paths):
        self.show_hidden = load_settings()["show_hidden_files"]
        if (self.show_hidden):
            return paths
        else :
            return [path for path in paths if not path.name.startswith('.')]

    
    def on_directory_tree_directory_selected(self,event:DirectoryTree.DirectorySelected):
        self.auto_expand = False
    
    
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

def load_settings():
    try:
        with open(settings_loc,'r') as setfile:
            data = setfile.read().strip()
            return json.loads(data) 
    except (json.JSONDecodeError,FileNotFoundError) as e:
        logger.error(f'{e} Function: {load_settings.__name__} in {Path(__file__).name}')
    
    

