from textual.widgets import RichLog,DataTable,Input
from textual.containers import Container,Vertical
from textual import on
from os import chdir,listdir
from pathlib import Path
from ..logger_config import logger


from .directory_tree import DTree

class Directory_tree_container(Container):
    def compose(self):
        self.dtree = DTree(path='/home/balaji/testings',id='dt')
        yield self.dtree
        chdir(self.dtree.path)

    # @on(Input.Changed)
    # def on_input_changed(self,event:Input.Changed):
    #     list_path = listdir(self.dtree.path)
    #     a = [Path(path) for path in list_path if path.startswith(event.value)]
    #     self.dtree.filter_paths(a)
    #     self.dtree.refresh()
    #     logger.info('hello wrold')
        

class Background_process_container(Container):
    def compose(self):
        self.dtable = DataTable(id='process_table')
        with Vertical():
            yield self.dtable
    
    def on_mount(self):
        self.dtable.add_columns('PID','Command','Status')

