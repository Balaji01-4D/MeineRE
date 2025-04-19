import csv
import json
from pathlib import Path

from textual.widgets import TextArea, Static
from textual.screen import ModalScreen
from textual.containers import Container
from textual.worker import Worker

SYNTAX_HIGHLIGHTING_SUPPORTED_FILES: dict[str, str] = {
    ".py": "python",
    ".java": "java",
    ".css": "css",
    ".html": "html",
    ".json": "json",
    ".rs": "rust",
    ".go": "go",
    ".sql": "sql",
    ".xml": "xml",
    ".toml": "toml",
    ".md": "markdown",
    ".yaml": "yaml",
    ".markdown": "markdown",
    ".htm": "html",
    ".sh": "bash",
    ".yml": "yaml",
}

PROGRAMMING_AND_SCRIPTING_LANGUAGES: set[str] = {
    ".c",
    ".cpp",
    ".cs",
    ".kt",
    ".kts",
    ".pl",
    "swift",
    ".php",
    ".rb",
    ".ts",
    ".bat",
    ".cmd",
    ".ps1",
}

CONFIG_AND_DATA_FILES: set[str] = {
    ".csv",
    ".tsv",
    ".ini",
    ".env",
    ".conf",
    ".gitconfig",
}

DOCUMENTATION_AND_MIXED_CONTENT_FILES: set[str] = {
    ".rst",
    ".tex",
    ".adoc",
    ".log",
    ".txt",
}


class MeineTextAreaScreen(ModalScreen):

    CSS_PATH = Path(__file__).parent.parent / "tcss/app.tcss"

    def __init__(self, filepath: Path, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.filepath = filepath
        self.text_area_theme = self.app.SETTINGS["text_editor_theme"]

    def _on_mount(self):
        self.run_worker(self.read_file(), exclusive=True, group="reading-file")

    def compose(self):
        self.textarea = TextArea(
            show_line_numbers=True,
            read_only=True,
            id="text-area",
            theme=self.text_area_theme,
        )
        with Container():
            yield Static(str(self.filepath.name))
            yield self.textarea

    async def read_file(self) -> None:
        try:
            self.textarea.loading = True
            extension = self.filepath.suffix
            self.get_syntax_highlighting(extension)
            if extension == "csv":
                self.run_worker(self.read_csv_files(self.filepath))
            elif extension == "json":
                self.run_worker(self.read_json_files(self.filepath))
            else:
                self.run_worker(self.read_txt_files(self.filepath))
        except Exception as e:
            self.notify(f"{e}")

    def get_syntax_highlighting(self, extension: str) -> None:
        """sets a syntax highlighting based on the file extension & category"""
        if extension in SYNTAX_HIGHLIGHTING_SUPPORTED_FILES:
            self.textarea.language = SYNTAX_HIGHLIGHTING_SUPPORTED_FILES[extension]
        elif extension in PROGRAMMING_AND_SCRIPTING_LANGUAGES:
            self.textarea.language = "bash"
        elif extension in CONFIG_AND_DATA_FILES:
            self.textarea.language = "json"
        else:
            self.textarea.language = "markdown"

    async def read_csv_files(self, filepath: Path) -> None:
        try:
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                self.textarea.text = "\n".join([",".join(row) for row in reader])
        except Exception as e:
            self.textarea.text = ""
            self.notify(f"unsupported file format {e}")

    async def read_txt_files(self, filepath: str) -> None:
        try:
            with open(filepath, "r") as file:
                self.textarea.text = file.read()
        except Exception as e:
            self.textarea.text = ""
            self.notify(f"unsupported file format {e}")

    async def read_json_files(self, filepath: Path) -> None:
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                self.textarea.text = json.dumps(data, indent=4)
        except Exception as e:
            self.textarea.text = ""
            self.notify(f"unsupported file format {e}")

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.name == "read_file" and event.worker.is_finished:
            self.textarea.loading = False
