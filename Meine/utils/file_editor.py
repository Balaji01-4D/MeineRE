from json import dump
from pathlib import Path

history_loc = Path(__file__).parent.parent /'resources/history.json' 
settings_loc = Path(__file__).parent.parent /'resources/settings.json'


def save_history(history:list[str]) -> None:
    with open(history_loc,'w') as file:
        dump(history,file,indent=4)


def save_settings(settings: dict[str|bool]) -> None:
    with open(settings_loc,'w') as file:
        dump(settings,file,indent=4)


def main():
    ...

    


if __name__ == '__main__':
    main()