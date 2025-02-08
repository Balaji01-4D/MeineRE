import os
from pathlib import Path
from textual.binding import Binding
from textual.widgets import DirectoryTree

from Meine.utils.file_loaders import load_settings


class DTree(DirectoryTree):

    
    BINDINGS = [
                Binding('left','cd_parent_directory'),
                Binding('home','cd_home_directory',priority=True),
                Binding('right','select_focused_directory')
            ]
    

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
            self.text_area = self.screen.text_area
            self.file_path = event.path
            if (self.previous_file is None or self.previous_file != event.path):
                self.screen.show_textarea()
                self.text_area.filepath = self.file_path
                
                self.previous_file = event.path
                self.run_worker(self.text_area.read_file(),exclusive=True)
            elif (self.previous_file == event.path):
                self.screen.hide_textarea()
                self.previous_file = None
        except Exception as e:
            self.notify(f'Unsupported file format {e}')
            

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


