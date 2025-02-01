from textual.widgets import DirectoryTree
from textual.binding import Binding
from pathlib import Path
import os
from textual.widgets import TextArea
from Meine.exceptions import ErrorNotify
from textual.keys import Keys
from Meine.logger_config import logger
from Meine.utils.file_loaders import load_settings

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

    def on_directory_tree_file_selected(self,event:DirectoryTree.FileSelected):
        if (self.previous_file is None):
            self.text_area: TextArea = self.screen.replace_IO_TextArea(event.path)
            self.previous_file = event.path
        



        
    
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

