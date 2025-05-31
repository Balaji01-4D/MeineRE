from fileinput import filename
import json
import random
from pathlib import Path

import xdialog
from appdirs import user_data_dir
import importlib.resources as pkg_resources

from meine.exceptions import InfoNotify

APP_NAME = "meine"
# ------------------ USER PATHS ------------------

USER_DATA_DIR = Path(user_data_dir(APP_NAME))
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_JSON_PATH = USER_DATA_DIR / "history.json"
SETTINGS_JSON_PATH = USER_DATA_DIR / "settings.json"
CUSTOM_JSON_PATH = USER_DATA_DIR / "customs.json"
QUOTES_JSON_PATH = USER_DATA_DIR / "quotes.json"


DEFAULT_RESOURCES_PATH = pkg_resources.files("meine.resources")

# ------------------ INITIALIZE DEFAULTS IF MISSING ------------------

def _initialize_file_if_missing(target: Path, resource_file: str):
    """Copy default resource file to user directory if it doesn't exist."""
    if not target.exists():
        with DEFAULT_RESOURCES_PATH.joinpath(resource_file).open("rb") as default:
            target.write_bytes(default.read())

def initialize_user_data_files():
    _initialize_file_if_missing(HISTORY_JSON_PATH, "history.json")
    _initialize_file_if_missing(SETTINGS_JSON_PATH, "settings.json")
    _initialize_file_if_missing(CUSTOM_JSON_PATH, "customs.json")
    _initialize_file_if_missing(QUOTES_JSON_PATH, "quotes.json")

# ------------------ HISTORY ------------------

def save_history(history: list[str]) -> None:
    with open(HISTORY_JSON_PATH, "w") as file:
        json.dump(history, file, indent=4)

def clear_history() -> None:
    with open(HISTORY_JSON_PATH, "w") as file:
        json.dump([], file, indent=4)

def load_history() -> list[str]:
    with open(HISTORY_JSON_PATH, "r") as file:
        return json.load(file)

# ------------------ SETTINGS ------------------

def save_settings(settings: dict[str, str]) -> None:
    with open(SETTINGS_JSON_PATH, "w") as file:
        json.dump(settings, file, indent=4)

def load_settings() -> dict[str | str | bool]:
    with open(SETTINGS_JSON_PATH, "r") as file:
        return json.load(file)

# ------------------ PATH EXPANSIONS ------------------

def add_custom_path_expansion(Name: str | None = None) -> str:
    if not Name:
        raise InfoNotify("Need a Name")

    selected_path = xdialog.directory()
    data = load_Path_expansion()
    data.setdefault("path_expansions", {})[Name] = selected_path
    with open(CUSTOM_JSON_PATH, "w") as file:
        json.dump(data, file, indent=4)
    return f"{Name} = {selected_path} assigned successfully"

def load_Path_expansion() -> dict[str]:
    with open(CUSTOM_JSON_PATH, "r") as file:
        return json.load(file)

def load_custom_urls() -> dict[str]:
    with open(CUSTOM_JSON_PATH, "r") as file:
        return json.load(file).get("urls", {})

# ------------------ QUOTES ------------------

def load_random_quote() -> str:
    with open(QUOTES_JSON_PATH, "r") as file:
        quotes = json.load(file)
        if (quotes):
            return random.choice(quotes)
        return "Meine"



class Quotes:

    FILE_NAME = "quotes.json"

    DEFAULT_PATH = DEFAULT_RESOURCES_PATH.joinpath(FILE_NAME)

    USER_PATH = USER_DATA_DIR / FILE_NAME

    def __init__(self):
        pass

    def reset(self):
        with self.DEFAULT_PATH.open("rb") as file:
            self.USER_PATH.write_bytes(file.read())

    def clear(self):
        with self.USER_PATH.open("w") as file:
            json.dump([],file)

    def add_quote(self, quote):
        with self.USER_PATH.open("r") as file:
            quotes: list[str] = json.load(file)
        quotes.append(quote)
        with self.USER_PATH.open("w") as file:
            json.dump(quotes, file, indent=4)

