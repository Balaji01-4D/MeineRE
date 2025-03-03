from pathlib import Path
from re import search

import platformdirs
from textual.binding import Binding
from textual.widgets import Input, DirectoryTree

from Meine.utils.file_manager import load_Path_expansion

actions = [
    "uz",
    "z",
    "zip",
    "del",
    "c",
    "mk",
    "create",
    "make",
    "unzip",
    "delete",
    "copy",
    "cp",
    "rename",
    "rn",
]


class MeineInput(Input):

    BINDINGS = [
        Binding("up", "history_up", "navigate the history up", show=False),
        Binding("down", "history_down", "navigate the history down", show=False),
    ]

    def __init__(
        self,
        history,
        history_index,
        value=None,
        placeholder="",
        highlighter=None,
        password=False,
        *,
        restrict=None,
        type="text",
        max_length=0,
        suggester=None,
        validators=None,
        validate_on=None,
        valid_empty=False,
        select_on_focus=True,
        name=None,
        id=None,
        classes=None,
        disabled=False,
        tooltip=None,
    ):
        super().__init__(
            value,
            placeholder,
            highlighter,
            password,
            restrict=restrict,
            type=type,
            max_length=max_length,
            suggester=suggester,
            validators=validators,
            validate_on=validate_on,
            valid_empty=valid_empty,
            select_on_focus=select_on_focus,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            tooltip=tooltip,
        )
        self.history = history
        self.history_index = history_index

    def on_mount(self):
        self.directory_tree = self.screen.query_one(
            "#directory-tree", expect_type=DirectoryTree
        )

    def action_history_up(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)

    def on_input_changed(self):
        matched_keyword = search(r"(p|d)\{(.+)\}", self.value)
        if matched_keyword:
            prefix = matched_keyword.group(1)
            if prefix == "p":
                self.replace_with_path_expansion(matched_keyword.group(2))
            elif prefix == "d":
                self.replace_with_directory_node_name(matched_keyword.group(2))
        else:
            None

    def replace_with_directory_node_name(self, keyword: str) -> None:
        try:
            line = int(keyword)
        except:
            self.notify("Need a Integer")
            return
        replaced_by = self.directory_tree.get_node_at_line(line)
        if replaced_by:
            self.value = self.value.replace(
                f"d{{{keyword}}}", replaced_by.data.path.name
            )
        else:
            self.notify("Not Found")

    def replace_with_path_expansion(self, keyword: str):
        current_dir = Path.cwd()

        DEFAULT_PATH_EXPANSION: dict[str | Path] = {
            "home": Path.home(),
            "current": current_dir,
            "<-": current_dir.parent,
            "this": current_dir,
            "parent": current_dir.parent,
            "parent+": current_dir.parent.parent,
            "parent++": current_dir.parent.parent.parent,
            "downloads": platformdirs.user_downloads_dir(),
            "documents": platformdirs.user_documents_dir(),
            "desktop": platformdirs.user_desktop_dir(),
        }

        DEFAULT_PATH_EXPANSION |= load_Path_expansion()["path_expansions"]
        if keyword in DEFAULT_PATH_EXPANSION:
            ReplaceBy = str(DEFAULT_PATH_EXPANSION[keyword])
            self.value = self.value.replace(f"p{{{keyword}}}", ReplaceBy)
        else:
            self.notify(
                f"{keyword} Is Not Found and It Is Removed For Good.",
                severity="error",
                title="Not Found",
            )

    def action_history_down(self):
        try:

            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.value = self.history[self.history_index]
                self.cursor_position = len(self.value)

            else:
                self.history_index = len(self.history)
                self.value = ""
        except Exception as e:

            None

    def on_input_submitted(self):
        self.history_index += 1
