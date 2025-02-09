from pathlib import Path
import json

history_loc = Path(__file__).parent.parent / "resources/history.json"
settings_loc = Path(__file__).parent.parent / "resources/settings.json"
customs_loc = Path(__file__).parent.parent / "resources/customs.json"


def load_settings() -> dict[str | str | bool]:
    """loads the history from the resoruces/settings.json"""
    with open(settings_loc, "r") as settings_file:
        data = settings_file.read().strip()
        return json.loads(data)


def load_history() -> list[str]:
    """loads the history from the resoruces/history.json"""
    with open(history_loc, "r") as history_file:
        data = history_file.read().strip()
        return json.loads(data)


def load_Path_expansion() -> dict[str]:
    with open(customs_loc, "r") as path_exp:
        data = path_exp.read().strip()
        return json.loads(data)


def load_custom_urls() -> dict[str]:
    with open(customs_loc, "r") as file:
        text_data = file.read().strip()
        data = json.loads(text_data)
        return data["urls"]


def main():
    print(load_history())


if __name__ == "__main__":
    main()
