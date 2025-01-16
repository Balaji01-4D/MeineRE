from textual.app import App
from textual.widgets import Header, Footer, Button,DirectoryTree
from textual.containers import Vertical
import asyncio

class BackgroundTaskApp(App):
    """Main app to manage background tasks."""
    
    
    def __init__(self):
        super().__init__()
        self.tasks = {}  # Initialize tasks dictionary to store tasks by ID

    def compose(self):
        yield Header()
        yield DirectoryTree('./Meine')
        yield Footer()


if __name__ == "__main__":
    BackgroundTaskApp().run()


