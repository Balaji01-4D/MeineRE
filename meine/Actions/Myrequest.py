from meine.exceptions import InfoNotify


def GetName(Action):
    print(f"Need a File or Folder to {Action}")


def GetFile(Action):
    print(f"Need a File to {Action}")


def GetNewName(Action):
    print(f"Need a New Name to {Action}")


def GetDes(Action):
    print(f"Need a Destination to {Action}")


def GetTxt(Action):
    print(f"need a 'text' to {Action}")


def AlreadyExist(Source: str, Destination: str) -> str:
    """
    The file with name '< {Source} >' already exists in the '< {Destination} >' target directory
        Please choose a different name or Please choose another directory or location
    """
    raise InfoNotify(f"The file with name '< {Source} >' already exists in the '< {Destination} >' target directory .\nPlease choose a different name or Please choose another directory or location")
