from json import dump
from pathlib import Path
import xdialog
import asyncio

from Meine.exceptions import InfoNotify
from .file_loaders import load_Path_expansion

history_loc = Path(__file__).parent.parent /'resources/history.json' 
settings_loc = Path(__file__).parent.parent /'resources/settings.json'
custom_path_expansion_loc = Path(__file__).parent.parent /'resources/customs.json'



def save_history(history:list[str]) -> None:
    with open(history_loc,'w') as file:
        dump(history,file,indent=4)


def save_settings(settings: dict[str|bool]) -> None:
    with open(settings_loc,'w') as file:
        dump(settings,file,indent=4)

def add_custom_path_expansion(Name: str|None = None) -> None:
    if (not Name):
        raise InfoNotify('Need a Name')
    
    selected_path = xdialog.directory()
    data = load_Path_expansion()
    data['path_expansions'][Name] = selected_path
    with open(custom_path_expansion_loc,'w') as file:
        dump(data,file,indent=4)
    return f'{Name} = {selected_path} assigned successfully'

    

def main():
    add_custom_path_expansion('desk')
    


if __name__ == '__main__':
    main()