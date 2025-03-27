from pathlib import Path


def SizeHelper(Size: int) -> None:
    for unit in ["B", "KB", "MB", "GB"]:
        if Size < 1024:
            return f"{Size:.2f} {unit}"
        Size /= 1024


def Is_subsequence(Sub: str, Main: str) -> None:
    it = iter(Main)
    return all(item in it for item in Sub)


def CMDMapper(labels: list[str], text: list[str]) -> dict[str]:
    cdict = {}
    Backup = {"FILE": "NEWNAME", "FOLDER": "DESTINATION"}
    for label, val in zip(labels, text):
        if cdict.__contains__(label):
            cdict[Backup[label]] = val
        else:
            cdict[label] = val
    return cdict


from rich.console import Console
from rich.progress import BarColumn, Progress

console = Console()


def display_progress(data: dict, title: str):
    """
    Displays a progress bar in the terminal for given data.

    Args:
    - data (dict): A dictionary where keys are labels and values are percentages (0-100).
    - title (str): Title for the progress section.
    """
    console.rule(f"[bold green]{title}", characters=" ")
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(bar_width=30),
        "{task.percentage:>3.0f}%",
        console=console,
    ) as progress:
        tasks = {}
        # Create a progress bar for each data entry
        for label, percentage in data.items():
            tasks[label] = progress.add_task(
                f"[bold]{label}", total=100, completed=percentage
            )

        # Update each bar (in this static example, they're set initially)
        for label, percentage in data.items():
            progress.update(tasks[label], completed=percentage)
