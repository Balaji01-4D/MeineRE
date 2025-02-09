from pathlib import Path

from textual.containers import Container, Horizontal
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Select, Static, Switch


from Meine.Screens.me import Myself
from Meine.utils.file_editor import clear_history, save_settings
from Meine.utils.file_loaders import load_settings


class Settings(ModalScreen):

    def __init__(self, name=None, id=None, classes=None):
        self.text_area = self.app.query_one("#text_editor")
        self.app_settings = self.app.SETTINGS
        super().__init__(name, id, classes)

    CSS_PATH = Path(__file__).parent.parent / "tcss/setting.css"

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

        text_editor_mode_startup = self.app_settings["text_editor_mode_read_only"]

        self.select_text_editor_theme = Select(
            [(themes, themes) for themes in self.AVAILABLE_THEMES],
            prompt="choose a theme",
            allow_blank=False,
            id="select-text-editor-theme",
        )

        self.select_app_theme = Select(
            [(themes, themes) for themes in self.app._registered_themes.keys()],
            prompt="choose a theme",
            allow_blank=False,
            id="select-app-theme",
        )
        self.select_text_editor_language = Select(
            [(lang, lang) for lang in self.AVAILABLE_LANGUAGES],
            prompt="choose a language",
            allow_blank=False,
            id="select-text-editor-language",
        )
        self.select_text_editor_mode = Select(
            options=[("read", True), ("read and write", False)],
            value=text_editor_mode_startup,
            prompt="choose a text editor mode",
            allow_blank=False,
            id="select-text-editor-mode",
        )

        yield Container(
            Static("settings", id="settings-title"),
            Horizontal(
                Static("show hidden files", classes="caption"),
                Switch(
                    id="hidden_files_sw", value=self.app_settings["show_hidden_files"]
                ),
            ),
            Horizontal(
                Static("clear history", classes="caption"),
                Button(label="clear", id="clear_history_bt"),
            ),
            Horizontal(
                Static("text app theme", classes="caption"), self.select_app_theme
            ),
            Horizontal(
                Static("text editor theme", classes="caption"),
                self.select_text_editor_theme,
            ),
            Horizontal(
                Static("text editor language", classes="caption"),
                self.select_text_editor_language,
            ),
            Horizontal(
                Static("text editor mode", classes="caption"),
                self.select_text_editor_mode,
            ),
            Button(label="About me", variant="success", id="about_me_bt"),
        )

    def on_click(self, event: Click):
        if str(event.widget.id) == "settings-screen":
            self.dismiss()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "about_me_bt":
            self.dismiss()
            self.app.push_screen(Myself())
        if event.button.id == "clear_history_bt":
            clear_history()
            self.notify(f"Command history is cleared ,restart required (optional)!")

    def on_switch_changed(self, event: Switch.Changed):
        if event.switch.id == "hidden_files_sw":
            self.app_settings["show_hidden_files"] = event.value
        save_settings(self.app_settings)

    def _on_mount(self):
        self.select_text_editor_language.value = self.text_area.language
        self.select_text_editor_theme.value = self.text_area.theme
        self.select_app_theme.value = self.app.theme

    def on_select_changed(self, event: Select.Changed):
        if event.select.id == "select-text-editor-theme":
            self.text_area.theme = event.value
            self.app.SETTINGS["text_editor_theme"] = event.value
        elif event.select.id == "select-text-editor-language":
            self.text_area.language = event.value
        elif event.select.id == "select-app-theme":
            self.app.theme = event.value
            self.app.SETTINGS["app_theme"] = event.value
        elif event.select.id == "select-text-editor-mode":
            self.text_area.read_only = event.value
            self.app.SETTINGS["text_editor_mode_read_only"] = event.value

        save_settings(self.app.SETTINGS)


class NameGetterScreen(ModalScreen):

    CSS_PATH = Path(__file__).parent.parent / "tcss/setting.css"

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
