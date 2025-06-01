from fileinput import filename
import json
import random
from pathlib import Path
from functools import lru_cache
from typing import Any, Dict, List, Optional

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

# Cache for frequently accessed data
_settings_cache: Optional[Dict[str, Any]] = None
_history_cache: Optional[List[str]] = None
_custom_cache: Optional[Dict[str, Any]] = None
_quotes_cache: Optional[List[str]] = None

def _read_json_file(path: Path) -> Any:
    """Read JSON file with error handling."""
    try:
        with open(path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # If file is corrupted, return empty default
        return {} if path.suffix == ".json" else []
    except FileNotFoundError:
        return {} if path.suffix == ".json" else []

def _write_json_file(path: Path, data: Any) -> None:
    """Write JSON file with error handling."""
    try:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
    except (OSError, json.JSONDecodeError) as e:
        raise InfoNotify(f"Failed to write to {path.name}: {str(e)}")

def _initialize_file_if_missing(target: Path, resource_file: str) -> None:
    """Copy default resource file to user directory if it doesn't exist."""
    if not target.exists():
        try:
            with DEFAULT_RESOURCES_PATH.joinpath(resource_file).open("rb") as default:
                target.write_bytes(default.read())
        except OSError as e:
            raise InfoNotify(f"Failed to initialize {resource_file}: {str(e)}")

def initialize_user_data_files() -> None:
    """Initialize all user data files with error handling."""
    for path, filename in [
        (HISTORY_JSON_PATH, "history.json"),
        (SETTINGS_JSON_PATH, "settings.json"),
        (CUSTOM_JSON_PATH, "customs.json"),
        (QUOTES_JSON_PATH, "quotes.json")
    ]:
        _initialize_file_if_missing(path, filename)

# ------------------ HISTORY ------------------

def save_history(history: List[str]) -> None:
    """Save history with caching."""
    global _history_cache
    _write_json_file(HISTORY_JSON_PATH, history)
    _history_cache = history

def clear_history() -> None:
    """Clear history with cache update."""
    global _history_cache
    _write_json_file(HISTORY_JSON_PATH, [])
    _history_cache = []

@lru_cache(maxsize=1)
def load_history() -> List[str]:
    """Load history with caching."""
    global _history_cache
    if _history_cache is None:
        _history_cache = _read_json_file(HISTORY_JSON_PATH)
    return _history_cache

# ------------------ SETTINGS ------------------

def save_settings(settings: Dict[str, Any]) -> None:
    """Save settings with caching."""
    global _settings_cache
    _write_json_file(SETTINGS_JSON_PATH, settings)
    _settings_cache = settings

@lru_cache(maxsize=1)
def load_settings() -> Dict[str, Any]:
    """Load settings with caching."""
    global _settings_cache
    if _settings_cache is None:
        _settings_cache = _read_json_file(SETTINGS_JSON_PATH)
    return _settings_cache

# ------------------ PATH EXPANSIONS ------------------

def add_custom_path_expansion(Name: Optional[str] = None) -> str:
    """Add custom path expansion with validation."""
    if not Name:
        raise InfoNotify("Need a Name")

    selected_path = xdialog.directory()
    if not selected_path:
        raise InfoNotify("No directory selected")

    data = load_Path_expansion()
    data.setdefault("path_expansions", {})[Name] = selected_path
    _write_json_file(CUSTOM_JSON_PATH, data)

    # Update cache
    global _custom_cache
    _custom_cache = data

    return f"{Name} = {selected_path} assigned successfully"

@lru_cache(maxsize=1)
def load_Path_expansion() -> Dict[str, Any]:
    """Load path expansions with caching."""
    global _custom_cache
    if _custom_cache is None:
        _custom_cache = _read_json_file(CUSTOM_JSON_PATH)
    return _custom_cache

@lru_cache(maxsize=1)
def load_custom_urls() -> Dict[str, str]:
    """Load custom URLs with caching."""
    data = load_Path_expansion()
    return data.get("urls", {})

# ------------------ QUOTES ------------------

@lru_cache(maxsize=1)
def load_random_quote() -> str:
    """Load random quote with caching."""
    global _quotes_cache
    if _quotes_cache is None:
        _quotes_cache = _read_json_file(QUOTES_JSON_PATH)

    if not _quotes_cache:
        return "Meine"

    return random.choice(_quotes_cache)



class Quotes:

    FILE_NAME = "quotes.json"

    DEFAULT_PATH = DEFAULT_RESOURCES_PATH.joinpath(FILE_NAME)

    USER_PATH = USER_DATA_DIR / FILE_NAME

    def __init__(self):
        pass

    def reset(self) -> None:
        """Reset quotes to default."""
        try:
            with self.DEFAULT_PATH.open("rb") as file:
                self.USER_PATH.write_bytes(file.read())
            # Clear cache
            global _quotes_cache
            _quotes_cache = None
        except OSError as e:
            raise InfoNotify(f"Failed to reset quotes: {str(e)}")

    def clear(self) -> None:
        """Clear all quotes."""
        _write_json_file(self.USER_PATH, [])
        # Clear cache
        global _quotes_cache
        _quotes_cache = []

    def add_quote(self, quote: str) -> None:
        """Add a new quote."""
        global _quotes_cache
        quotes = _quotes_cache if _quotes_cache is not None else _read_json_file(self.USER_PATH)
        quotes.append(quote)
        _write_json_file(self.USER_PATH, quotes)
        _quotes_cache = quotes

