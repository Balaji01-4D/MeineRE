from textual.widgets import RichLog,DataTable
from textual.containers import Container,Vertical
from os import chdir


from .directory_tree import DTree

class Directory_tree_container(Container):
    def compose(self):
        dtree = DTree(path='/home/balaji/testings',id='dt')
        self.dtree_log = RichLog(id='dtree_log')
        yield dtree
        chdir(dtree.path)

class Background_process_container(Container):
    def compose(self):
        self.dtable = DataTable(id='process_table')
        with Vertical():
            yield self.dtable
    
    def on_mount(self):
        self.dtable.add_columns('PID','Command','Status')

