import xdialog
from pathlib import Path

custom_path_expansion = Path(__file__).parent.parent /'resources/custom_path_exp.json'

def add_path_expansion():
    print(xdialog.directory())

def main():
    get_path()


if __name__ == '__main__':
    main()