from textual.widgets import RichLog,DataTable,Input
from textual.containers import Container,Vertical
from os import chdir,listdir
from pathlib import Path
from ..logger_config import logger
from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget


from .directory_tree import DTree

class Directory_tree_container(Container):

    def __init__(self, *children, name = None, id = None, classes = None, disabled = False):
        self.dtree = DTree(path='/home/balaji/testings',id='dt')

        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self):
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



from __future__ import annotations

import getpass
import os
import socket



class HeaderCurrentPath(Widget):
    path = reactive(None, layout=True)

    def render(self) -> RenderableType:
        if not self.path:
            return ""

        path = str(self.path.name)
        root = str(self.path.parent) + os.path.sep
        return Text.assemble((root, "dim"), (path, "bold"))


class HeaderHost(Widget):
    def render(self) -> RenderableType:
        return "[dim]@[/]" + socket.gethostname()


class HeaderUser(Widget):
    def render(self) -> RenderableType:
        return getpass.getuser()


class Header(Widget):
    def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)

    def compose(self) -> ComposeResult:
        yield HeaderUser(id="header-user")
        yield HeaderHost(id="header-host")
        yield HeaderCurrentPath(id="header-current-path")


class CodeEditor(Container):
    ...