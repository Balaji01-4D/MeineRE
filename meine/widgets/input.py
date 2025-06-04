from pathlib import Path
import os
from re import search

import platformdirs
from textual.binding import Binding
from textual.widgets import Input, DirectoryTree
from textual.suggester import SuggestFromList

from meine.utils.file_manager import load_Path_expansion

actions = [
    "cd",
    "rm",
    "uz",
    "z",
    "zip",
    "del",
    "c",
    "mk",
    "create",
    "make",
    "mv",
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

    suggestions = []

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

    def _get_hint_text(self) -> tuple[list[str], str | None, str]:
        try:
            first, *rest = self.value.split(maxsplit=2)
            if first not in actions:
                return [], None, " "

            if not rest:
                return [first], None, " "

            hint = rest[-1]
            if len(rest) == 1 and hint.endswith(','):
                return [first, hint], None, ""

            return rest[:-1] + [first], hint, " "
        except ValueError:
            return [], None, " "

    def suggestion_provider(self, hint: str | None = None) -> list[str]:
        try:
            items = os.scandir('.')
            if hint:
                hint_lower = hint.lower()
                return [item.name for item in items if item.name.lower().startswith(hint_lower)]
            return [item.name for item in items]
        except OSError:
            return []

    def on_input_changed(self) -> None:
        if not self.value:
            self.suggestions.clear()
            self.suggester = None
            return

        matched_keyword = search(r"\{(.+)\}", self.value)
        if matched_keyword:
            self.replace_with_path_expansion(matched_keyword.group(1))

        self.suggestions, hint, separator = self._get_hint_text()
        if self.suggestions:
            current_value = self.value.lower()
            suggestions = [
                " ".join(self.suggestions) + separator + item
                for item in self.suggestion_provider(hint)
                if item.lower() not in current_value
            ]
            if suggestions:
                self.suggester = SuggestFromList(suggestions, case_sensitive=False)
            else:
                self.suggester = None

    def key_backspace(self):
        self.suggestions.clear()

    def action_history_up(self) -> None:
        """Optimized history navigation up."""
        if self.history_index > 0:
            self.history_index -= 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)

    def action_history_down(self) -> None:
        """Optimized history navigation down."""
        if not self.history:
            return

        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.value = self.history[self.history_index]
        else:
            self.history_index = len(self.history)
            self.value = ""

        self.cursor_position = len(self.value)

    def on_input_submitted(self) -> None:
        """Optimized input submission handler."""
        if self.value.strip():  # Only increment history for non-empty inputs
            self.history_index += 1
        self.suggestions.clear()
        self.suggester = None


    def replace_with_path_expansion(self, keyword: str) -> None:
        """Optimized path expansion replacement with cached paths."""
        current_dir = Path.cwd()

        if not hasattr(self, '_default_paths'):
            self._default_paths = {
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
            self._default_paths.update(load_Path_expansion().get("path_expansions", {}))

        if path := self._default_paths.get(keyword):
            self.value = self.value.replace(f"{{{keyword}}}", str(path))
        else:
            self.notify(
                f"Path expansion '{keyword}' not found",
                severity="error",
                title="Not Found"
            )
