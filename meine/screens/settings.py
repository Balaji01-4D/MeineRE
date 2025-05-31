from pathlib import Path

from textual.containers import Container, Horizontal
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Select, Static, Switch


from meine.screens.me import Myself
from meine.utils.file_manager import clear_history


class Settings(ModalScreen):

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

    CSS_PATH = Path(__file__).parent.parent / "tcss/setting.tcss"

    AVAILABLE_THEMES = {"dracula", "github_light", "monokai", "vscode_dark", "css"}

    AVAILABLE_LANGUAGES = {
        "json",
        "markdown",
        "go",
        "javascript",
        "yaml",
        "regex",
        "bash",
        "rust",
        "toml",
        "python",
        "css",
        "html",
        "java",
        "xml",
        "sql",
    }

    def compose(self):

        self.select_app_theme = Select(
            [(themes, themes) for themes in self.app._registered_themes.keys()],
            prompt="choose a theme",
            allow_blank=False,
            id="select-app-theme",
        )

        self.select_text_area_theme = Select(
            [(themes, themes) for themes in self.AVAILABLE_THEMES],
            prompt="choose a theme",
            allow_blank=False,
            id="select-text-area-theme",
            value=self.app.SETTINGS["text_editor_theme"],
        )

        self.select_directory_tree_dock = Select(
            [("left", "left"), ("right", "right")],
            id="select-directory-tree-container-dock",
            prompt="directory tree dock",
            allow_blank=False,
            value=self.app.SETTINGS["directory-tree-dock"],
        )

        yield Container(
            Static("SETTINGS", id="settings-title"),
            Horizontal(
                Static("show hidden files", classes="caption"),
                Switch(
                    id="hidden_files_sw", value=self.app.SETTINGS["show_hidden_files"]
                ),
            ),
            Horizontal(
                Static("clear history", classes="caption"),
                Button(label="clear", id="clear_history_bt"),
            ),
            Horizontal(Static("App theme", classes="caption"), self.select_app_theme),
            Horizontal(
                Static("text area theme", classes="caption"),
                self.select_text_area_theme,
            ),
            Horizontal(
                Static("directory tree position", classes="caption"),
                self.select_directory_tree_dock,
            ),
            Button(
                label="About me",
                variant="success",
                id="about_me_bt",
                tooltip="about the developer",
            ),
        )

    def on_click(self, event: Click) -> None:
        """close the screen if the click received from outside of settings screen"""
        if str(event.widget.id) == "settings-screen":
            self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """clear the history or push the screen of developer page"""
        if event.button.id == "about_me_bt":
            self.dismiss()
            self.app.push_screen(Myself())
        if event.button.id == "clear_history_bt":
            clear_history()
            self.app.HISTORY = []
            self.notify(f"Command history is cleared")

    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id == "hidden_files_sw":
            self.app.SETTINGS["show_hidden_files"] = event.value

    def _on_mount(self) -> None:
        self.select_app_theme.value = self.app.theme

    def on_select_changed(self, event: Select.Changed) -> None:
        select_id = event.select.id
        if select_id == "select-text-area-theme":
            self.app.SETTINGS["text_editor_theme"] = event.value

        elif select_id == "select-app-theme":
            self.app.theme = event.value
            self.app.SETTINGS["app_theme"] = event.value

        elif select_id == "select-directory-tree-container-dock":
            self.app.screen_stack[1].query_one(
                "#directory-tree-container"
            ).styles.dock = event.value
            self.app.SETTINGS["directory-tree-dock"] = event.value


class NameGetterScreen(ModalScreen):

    CSS_PATH = Path(__file__).parent.parent / "tcss/setting.tcss"

    def __init__(self, title, callback, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.callback = callback
        self.title = title

    def compose(self):
        with Container():
            yield Static(self.title, id="title")
            yield Input(id="Input_of_utils")

    def on_input_submitted(self, event: Input.Submitted):
        self.app.pop_screen()
        result = self.callback(event.value)
        self.app.notify(result)
