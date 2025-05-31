import re
from pathlib import Path
from re import Match, Pattern

from rich.table import Table

from meine.Actions import File, System, Zip
from meine.exceptions import InfoNotify

d: dict[str, Pattern] = {
    "twopath": re.compile(r"""(c|m|mv|cp|copy|move)\s+(.+)\s+(?:to)\s+(.+)"""),
    "onepath": re.compile(r"""(d|rm|r|del|mk|mkdir|mkd|create|delete|clr|show)\s+(.+)"""),
    "rename": re.compile(r"(rename|rn)\s+(.+)\s+(?:as|to)\s+(.+)"),
    "system": re.compile(
        r"(battery|bt|charge|user|me|env|ip|cpu|disk|ram|net|time|system|sys|cpu|disk|storage|net|process)\s?(\s[^\s]+)?"
    ),
    "search_text": re.compile(r"""(find|where|search)\s+["'](.+)["']\s+(.+)"""),
    "notepad": re.compile(r"(write|notepad|wr)\s+(.+)"),
    "compress": re.compile(r"""(z|uz|zip|tar|gz|7z|unzip)\s+(.+)"""),
    "backup": re.compile(r"""(backup|bk)\s+(.+)"""),
}

files = File()
systems = System()
zips = Zip()


async def CLI(Command):

    async def handle_rename(RegexMatch: Match):
        source_unknown_type: str = RegexMatch.group(2)
        newname_unknown_type: str = RegexMatch.group(3)
        source: str | list = (
            source_unknown_type.split(",")
            if "," in source_unknown_type
            else source_unknown_type
        )
        newname: str | list = (
            newname_unknown_type.split(",")
            if "," in newname_unknown_type
            else newname_unknown_type
        )

        if isinstance(source, list) and isinstance(newname, list):
            results = [await Rename(s, n) for s, n in zip(source, newname)]
            return "\n".join(results)
        elif not isinstance(source, list) and isinstance(newname, list):
            raise InfoNotify("[#E06C75]Multiple Source Need to Rename Multiple")
        elif isinstance(source, list) and not isinstance(newname, list):
            raise InfoNotify("[#E06C75]Multiple New Name Need to Rename Multiple")
        else:
            return await Rename(source, newname)

    async def handle_two_path(RegexMatch: Match):
        act: str = RegexMatch.group(1)
        source_unknown_type = RegexMatch.group(2)
        source: str | list = (
            source_unknown_type.split(",")
            if "," in source_unknown_type
            else source_unknown_type
        )
        destination: str = RegexMatch.group(3)
        if act in {"cp", "copy", "c"}:
            if isinstance(source, list):
                results = [await Copy(s, destination) for s in source]
                return "\n".join(results)
            return await Copy(source, destination)
        else:  # Handle move
            if isinstance(source, list):
                results = [await Move(s, destination) for s in source]
                return "\n".join(results)
            return await Move(source, destination)

    async def handle_one_path(RegexMatch: Match):
        act = RegexMatch.group(1)
        source_unknown_type = RegexMatch.group(2)
        source: str | list = (
            source_unknown_type.split(",")
            if "," in source_unknown_type
            else source_unknown_type
        )

        if act in {"delete", "del", "d",'rm'}:
            if isinstance(source, list):
                results = [await Delete(s) for s in source]
                return "\n".join(results)
            return await Delete(source)

        elif act in {"mk", "create", "make"}:
            if isinstance(source, list):
                results = [await Create(s, "file") for s in source]
                return "\n".join(results)
            return await Create(source, "file")

        elif act in {"mkdir","mkd"}:
            if isinstance(source, list):
                results = [await Create(s) for s in source]
                return "\n".join(results)
            return await Create(source)

        elif act == "show":
            if isinstance(source, list):
                raise InfoNotify("show file content accepts a single file")
            return await files.ShowContent_File(Path(source))

        elif act == "clr":
            if isinstance(source, list):
                results = [await files.ClearContent_File(Path(s)) for s in source]
                return "\n".join(results)
            return await files.ClearContent_File(Path(source))

    async def handle_system(RegexMatch: Match):
        act = RegexMatch.group(1)
        extra = RegexMatch.group(2)

        system_actions = {
            "ip": systems.IP,
            "ram": systems.RAMInfo,
            "time": systems.Time,
            "date": systems.Time,
            "disk": systems.DiskInfo,
            "storage": systems.DiskInfo,
            "space": systems.DiskInfo,
            "home": systems.HomeDir,
            "sys": systems.SYSTEM,
            "system": systems.SYSTEM,
            "bt": systems.Battery,
            "power": systems.Battery,
            "battery": systems.Battery,
            "net": systems.NetWork,
            "network": systems.NetWork,
            "env": systems.ENV,
            "cpu": systems.CPU,
            "usr": systems.USER,
            "user": systems.USER,
            "me": systems.USER,
            "process": systems.Processes,
            "background": systems.Processes,
            "kill": lambda: systems.ProcessKill(extra),
            "shutdown": lambda: systems.shutdown(extra),
        }

        if act in system_actions:
            return await system_actions[act]()
        raise (f"[#E06C75]Unknown system action: {act}")

    async def handle_compress(RegexMatch: Match) -> str:
        act: str = RegexMatch.group(1)
        source_unknown: str = RegexMatch.group(2)
        srcs: list | str = (
            source_unknown.split(",") if "," in source_unknown else source_unknown
        )

        if act in {"unzip", "uz"}:
            if isinstance(srcs, list):
                results = [await zips.Extract(Path(s)) for s in srcs]
                return "\n".join(results)
            return await zips.Extract(Path(srcs))

        else:
            if isinstance(srcs, list):
                results = [await zips.Compress(Path(s), format=act) for s in srcs]
                return "\n".join(results)

            return await zips.Compress(Path(srcs), format=act)

    async def handle_text_find(RegexMatch: Match) -> str | Table:
        text = RegexMatch.group(2)
        source = Path(RegexMatch.group(3))
        if source.is_dir():
            return await files.Text_Finder_Directory(text, source)
        elif source.is_file():
            return await files.Text_Finder_File(text, source)
        else:
            raise InfoNotify("Source Not Found")

    # Command-to-handler mapping
    handlers = {
        "rename": handle_rename,
        "twopath": handle_two_path,
        "onepath": handle_one_path,
        "system": handle_system,
        "compress": handle_compress,
        "search_text": handle_text_find,
    }

    for key, pattern in d.items():
        RegexMatch = pattern.match(Command)
        if RegexMatch:
            if key in handlers:
                return await handlers[key](RegexMatch)

    raise InfoNotify("Command not recognized.")


async def Copy(Source: str, Destination: str) -> str:
    sourcePath = Path(Source.strip("'"))
    destinationPath = Path(Destination.strip("'"))
    if destinationPath.is_dir():
        if sourcePath.is_file():
            result = await files.Copy_File(sourcePath, destinationPath)
            return result
        elif sourcePath.is_dir():
            result = await files.Copy_Folder(sourcePath, destinationPath)
            return result
        else:
            raise InfoNotify(f"{Source} Not Found")
    elif destinationPath.is_file():
        raise InfoNotify(f"{destinationPath} is a File")
    else:
        raise InfoNotify(f"{destinationPath.name} Not Found")


async def Move(Source: str, Destination: str) -> str:
    sourcePath = Path(Source.strip("'"))
    destinationPath = Path(Destination.strip("'"))
    if destinationPath.is_dir():
        if sourcePath.is_file():
            result = await files.Move_File(sourcePath, destinationPath)
            return result
        elif sourcePath.is_dir():
            result = await files.Move_Folder(sourcePath, destinationPath)
            return result
        else:
            raise InfoNotify(f"{Source} Not Found")
    elif destinationPath.is_file():
        raise InfoNotify(f"{destinationPath.name} is a File")
    else:
        raise InfoNotify(f"{destinationPath.name} Not Found")


async def Rename(Source: str, Newname: str) -> str:
    sourcePath = Path(Source.strip("'"))
    NewnamePath = Path(Newname.strip("'"))
    if sourcePath.is_file():
        result = await files.Rename_file(sourcePath, NewnamePath)
        return result
    elif sourcePath.is_dir():
        result = await files.Rename_file(sourcePath, NewnamePath)
        return result
    else:
        raise InfoNotify(f"{Source} Not Found")


async def Delete(Source: str) -> str:
    sourcePath: Path = Path(Source.strip("'"))
    if sourcePath.is_file():
        result = await files.Delete_File(sourcePath)
        return result
    elif sourcePath.is_dir():
        result = await files.Delete_Folder(sourcePath)
        return result
    else:
        raise InfoNotify(f"{Source} Not Found")


async def Create(source: str, hint="folder") -> str:
    source = source.strip("'")
    if hint != "folder":
        result = await files.Create_File(Path(source))
        return result
    else:
        result = await files.Create_Folder(Path(source))
        return result
