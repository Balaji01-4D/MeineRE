import json

import xdialog



def add_custom_path_expansion(Name: str|None = None) -> None:
    if (not Name):
        raise KeyError('no name')
    
    selected_path = xdialog.directory()
    data = load_Path_expansion()
    data['path_expansions'][Name] = selected_path
    with open(custom_path_expansion_loc,'w') as file:
        dump(data,file,indent=4)
    return f'{Name} = {selected_path} assigned successfully'

    