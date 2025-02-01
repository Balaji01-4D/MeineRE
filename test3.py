from textual.app import App, ComposeResult
from textual.widgets import TextArea, Button, Static
from textual.worker import Worker, get_current_worker
from textual import work
import os

class CustomTextEditor(TextArea):
    """
    A custom text editor widget that extends TextArea to support file loading.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = None  # Track the currently loaded file

    @work(thread=True)
    def load_file_async(self, file_path: str) -> str:
        """
        Load a file asynchronously in a worker thread.
        """
        worker = get_current_worker()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        if self.is_binary_file(file_path):
            raise ValueError(f"The file '{file_path}' is binary or unsupported.")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            return content
        except Exception as e:
            raise ValueError(f"Error reading file '{file_path}': {e}")

    def is_binary_file(self, file_path: str) -> bool:
        """
        Check if a file is binary by reading a small chunk of data.
        """
        try:
            with open(file_path, "rb") as file:
                chunk = file.read(1024)
                if b"\x00" in chunk:  # Null bytes indicate a binary file
                    return True
        except Exception:
            return True
        return False

    async def load_file(self, file_path: str) -> None:
        """
        Load a file into the text editor.
        """
        self.file_path = file_path
        self.notify("Loading file...")
        text = await self.load_file_async(file_path)
        self.text = text

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """
        Handle the worker state change event to update the text editor.
        """
        if event.worker.is_finished:
            if event.worker.result:
                self.text = event.worker.result
                self.notify(f"File '{self.file_path}' loaded successfully.")
            elif event.worker.error:
                self.notify(f"Error: {event.worker.error}")

    def notify(self, message: str) -> None:
        """
        Display a notification message (e.g., in a status bar or log).
        """
        self.app.query_one("#message", Static).update(message)


class TextEditorApp(App):
    """
    A Textual app that uses the CustomTextEditor widget.
    """

    def compose(self) -> ComposeResult:
        # Create the custom text editor
        self.editor = CustomTextEditor(language="plaintext", id="text-editor")
        yield self.editor

        # Create a Button to trigger file loading
        yield Button("Load File", id="load-file")

        # Create a Static widget for displaying messages
        yield Static("", id="message")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle the button press event to load a file.
        """
        self.notify("button prews")
        if event.button.id == "load-file":
            file_path = "./requirements.txt"  # Replace with your file path
            self.editor.load_file(file_path)

# Run the app
if __name__ == "__main__":
    app = TextEditorApp()
    app.run()