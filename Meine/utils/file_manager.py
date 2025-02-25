import json
from json import dump
from pathlib import Path

import xdialog

from Meine.exceptions import InfoNotify

HISTORY_JSON_PATH: Path = Path(__file__).parent.parent / "resources/history.json"
SETTINGS_JSON_PATH: Path = Path(__file__).parent.parent / "resources/settings.json"
CUSTOM_PATH_EXPANSION_JSON_PATH: Path = Path(__file__).parent.parent / "resources/customs.json"


def save_history(history: list[str]) -> None:
    """save history by passing a new list of history"""
    with open(HISTORY_JSON_PATH, "w") as file:
        dump(history, file, indent=4)


def clear_history() -> None:
    """clear history by dumping a empty list [] in the history json file"""
    with open(HISTORY_JSON_PATH, "w") as file:
        json.dump([], file, indent=4)


def save_settings(settings: dict[str,str]) -> None:
    """save the settings by passing the new settings"""
    with open(SETTINGS_JSON_PATH, "w") as file:
        dump(settings, file, indent=4)


def add_custom_path_expansion(Name: str | None = None) -> None:
    if not Name:
        raise InfoNotify("Need a Name")

    selected_path = xdialog.directory()
    data = load_Path_expansion()
    data["path_expansions"][Name] = selected_path
    with open(CUSTOM_PATH_EXPANSION_JSON_PATH, "w") as file:
        dump(data, file, indent=4)
    return f"{Name} = {selected_path} assigned successfully"


def load_settings() -> dict[str | str | bool]:
    """loads the history from the resoruces/settings.json"""
    with open(SETTINGS_JSON_PATH, "r") as settings_file:
        data = settings_file.read().strip()
        return json.loads(data)


def load_history() -> list[str]:
    """loads the history from the resoruces/history.json"""
    with open(HISTORY_JSON_PATH, "r") as history_file:
        data = history_file.read().strip()
        return json.loads(data)


def load_Path_expansion() -> dict[str]:
    with open(CUSTOM_PATH_EXPANSION_JSON_PATH, "r") as path_exp:
        data = path_exp.read().strip()
        return json.loads(data)


def load_custom_urls() -> dict[str]:
    with open(CUSTOM_PATH_EXPANSION_JSON_PATH, "r") as file:
        text_data = file.read().strip()
        data = json.loads(text_data)
        return data["urls"]
