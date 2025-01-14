from textual.app import App
from textual.widgets import Header, Footer, Button, DataTable
from textual.containers import Vertical
import asyncio

class BackgroundTaskApp(App):
    """Main app to manage background tasks."""
    
    CSS = """
    DataTable {
        height: auto;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.tasks = {}  # Initialize tasks dictionary to store tasks by ID

    def compose(self):
        yield Header()
        yield Vertical(
            Button("Run Background Task", id="run-task-btn"),
            DataTable(id="task-table"),
        )
        yield Footer()

    def on_mount(self):
        # Prepare the task table
        task_table = self.query_one("#task-table")
        task_table.add_columns("Task ID", "Status", "Progress")

    async def on_button_pressed(self, event: Button.Pressed):
        """Handle button press to start a task."""
        if event.button.id == "run-task-btn":
            task_id = f"Task-{len(self.tasks) + 1}"  # Generate a unique task ID
            self.log(f"Starting {task_id}...")
            task = asyncio.create_task(self.add_task(task_id))
            self.tasks[task_id] = task

            # Schedule cleanup once the task is done
            task.add_done_callback(lambda t: self.cleanup_task(task_id))

    async def add_task(self, task_id: str):
        """Add and monitor a background task."""
        task_table = self.query_one("#task-table")

        # Add task to the table
        task_table.add_row(task_id, "Running", "0%")

        # Simulate a long-running task
        for i in range(1, 11):
            await asyncio.sleep(1)  # Simulate work
            task_table.update_cell(task_id, 2, f"{i * 10}%")  # Update progress

        # Mark as completed
        task_table.update_cell(task_id, 1, "Completed")

    def cleanup_task(self, task_id: str):
        """Remove completed tasks from tracking."""
        self.log(f"Cleaning up {task_id}...")
        if task_id in self.tasks:
            del self.tasks[task_id]  # Remove the task from the dictionary

if __name__ == "__main__":
    BackgroundTaskApp().run()
