import os
from pathlib import Path

from textual.binding import Binding
from textual.events import Click
from textual.widgets import DirectoryTree

from meine.screens.textarea import MeineTextAreaScreen
from meine.utils.file_manager import load_settings


class DTree(DirectoryTree):

    expand = False
    auto_expand = False

    BINDINGS = [
        # Binding("left", "cd_parent_directory"),
        Binding("home", "cd_home_directory", priority=True),
        # Binding("right", "select_focused_directory"),
    ]

    def __init__(self, path, *, name=None, id=None, classes=None, disabled=False):
        super().__init__(path, name=name, id=id, classes=classes, disabled=disabled)
        self.previous_file = None

    # def on_directory_tree_directory_selected(
    #     self, event: DirectoryTree.DirectorySelected
    # ):
    #     """if control is pressed and directory tree node is selected """
    #     self.screen.query_one(RichLog).write(f"{event.node}")
    #     """else """
    #     self.path = event.path

    def filter_paths(self, paths):
        self.show_hidden = load_settings()["show_hidden_files"]
        if self.show_hidden:
            return paths
        else:
            return [path for path in paths if not path.name.startswith(".")]

    # def on_tree_node_selected(self, event: DirectoryTree.NodeSelected):
    #     """if control is pressed and directory tree node is selected """
    #     self.screen.query_one(RichLog).write(f"{event.node}")
    #     """else """
    #     self.path = event.node.

    def action_cd_home_directory(self):
        self.path = Path.home()
        os.chdir(self.path)
        self.refresh()

    def action_select_focused_directory(self):
        try:
            focused_path = self.cursor_node.data.path
            if focused_path and focused_path.is_dir():
                self.path = focused_path
                os.chdir(self.path)
                self.refresh()
            elif focused_path.is_file():
                self.app.notify(
                    f"{focused_path.name} is a file", severity="information"
                )
            else:
                self.app.notify(f"select a folder", severity="warning")
        except PermissionError:
            self.app.notify(
                f"{focused_path.name} Permission Denied", severity="warning"
            )

    def action_cd_parent_directory(self):
        current_path = Path(self.path)
        self.path = current_path.resolve().parent
        os.chdir(self.path)
        self.refresh()

    def is_text_file(self, file_path: str | Path | os.PathLike, block_size=512) -> bool:
        """detects the file is text based or not"""
        try:
            with open(file_path, "rb") as file:
                chunk = file.read(block_size)

                if b"\x00" in chunk:
                    print("in chunk")
                    return False

                try:
                    chunk.decode("utf-8")
                except UnicodeDecodeError:
                    return False

                return True
        except Exception:
            return False

    # def _on_mouse_down(self, event: MouseDown):
    #     if event.ctrl:
    #         self.screen.handle_files_click_input(event.widget)
    #     else :
    #         time.sleep(0.2)
    #         self.notify(f"x = {event.x} y = {event.y} {self.cursor_node}")

    def on_clicks(self, event: Click):
        try:
            if event.ctrl:
                self.screen.handle_files_click_input(event.widget)
            else:
                selected_node = self.cursor_node
                if selected_node == self.root:
                    self.path = selected_node.parent
                elif selected_node.is_dir():
                    self.path = selected_node
                    os.chdir(self.path)
                elif selected_node.is_file():
                    if self.is_text_file(selected_node):
                        self.app.push_screen(
                            MeineTextAreaScreen(
                                filepath=selected_node, id="textarea-screen"
                            )
                        )
                    else:
                        self.notify("unsupported file format")
                else:
                    None

        except PermissionError:
            self.notify(title="Error", message="Permission Denied", severity="error")
        except:
            None
