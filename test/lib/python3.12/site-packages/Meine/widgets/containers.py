import os

from textual.containers import Container, Vertical
from textual.widgets import DataTable, Static
from textual.events import Click

from .directory_tree import DTree


class Directory_tree_container(Container):

    def __init__(self, *children, name=None, id=None, classes=None, disabled=False):
        self.dtree = DTree(path=os.getcwd(), id="directory-tree")

        super().__init__(
            *children, name=name, id=id, classes=classes, disabled=disabled
        )

    def compose(self):
        yield Static("Directory tree", id="directory-tree-container-header")
        yield self.dtree
        os.chdir(self.dtree.path)

    # @on(Input.Changed)
    # def on_input_changed(self,event:Input.Changed):
    #     list_path = listdir(self.dtree.path)
    #     a = [Path(path) for path in list_path if path.startswith(event.value)]
    #     self.dtree.filter_paths(a)
    #     self.dtree.refresh()
    #     logger.info('hello wrold')

    def _on_click(self, event: Click):
        if event.widget.id == "directory-tree-container-header":
            self.dtree.reload()


class Background_process_container(Container):
    def compose(self):
        self.dtable = DataTable(id="process_table")
        with Vertical():
            yield self.dtable

    def on_mount(self):
        self.dtable.add_columns("PID", "Command", "Status")
