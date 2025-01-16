from pathlib import Path
import json

history_loc = Path(__file__).parent.parent /'resources/history.json' 
settings_loc = Path(__file__).parent.parent /'resources/settings.json'
path_exapansion_loc = Path(__file__).parent.parent /'resources/custom_path_exp.json'

def load_settings() -> dict[str|str|bool]:
    ''' loads the history from the resoruces/settings.json '''
    with open(settings_loc,'r') as settings_file:
        data = settings_file.read().strip()
        return json.loads(data) 


def load_history() -> list[str]:
    ''' loads the history from the resoruces/history.json '''
    with open(history_loc,'r') as history_file:
        data = history_file.read().strip()
        return json.loads(data) 

def load_Path_expansion() -> dict[str]:
    with open(path_exapansion_loc,'r') as path_exp:
        data = path_exp.read().strip()
        return json.loads(data)

def main():
    print(load_history())


if __name__ == '__main__':
    main()