import asyncio
import os
import shutil as sl
from pathlib import Path
from typing import Coroutine

import aiofiles
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from meine.exceptions import InfoNotify
from .Myrequest import AlreadyExist
from .app_theme import get_theme_colors


def need_theme():
    return get_theme_colors()

class File:

    async def Delete_File(self, FileName: Path) -> Coroutine[None, None, str]:
        """
        Asynchronously deletes a file or delegates folder deletion.

        Args:
            FileName (Path): The path of the file or folder to delete.

        Returns:
            Coroutine[None, None, str]: A success or error message.
        """

        if FileName.is_dir():
            return self.Delete_Folder(FileName)
        if FileName.is_file():
            try:
                await asyncio.to_thread(FileName.chmod, 0o744)
                await asyncio.to_thread(FileName.unlink)
                return f"[{need_theme()["foreground"]}]{FileName.name} Deleted Successfully."
            except FileNotFoundError:
                raise InfoNotify(f"File Not found")
            except PermissionError:
                raise InfoNotify(f"Permission denied")
            except Exception as e:
                raise InfoNotify(f"Error In Deleting {FileName.name}: {e}")
        else:
            raise InfoNotify(f"File Not found")


    async def Move_File(
        self, Source: Path, Destination: Path
    ) -> Coroutine[None, None, str]:
        """
        Asynchronously moves a file to the specified destination.

        Args:
            Source (Path): The path of the file to move.
            Destination (Path): The target directory.

        Returns:
            Coroutine[None, None, str]: A success or error message.

        """
        Final = Destination / Source.name

        if Final.exists():
            return AlreadyExist(Final.name, Final.parent)

        if not Source.exists():
            raise InfoNotify(f"{Source.name} Not Found.")
        if not Destination.exists() or not Destination.is_dir():
            raise InfoNotify(f"{Destination.name} Is Not a Valid Directory.")
        try:
            await asyncio.to_thread(sl.move, Source, Final)
            return f"[{need_theme()["foreground"]}]{Source.name} Moved Successfully to {Destination.name}."
        except PermissionError:
            raise InfoNotify("Permission Denied.")
        except Exception as e:
            raise InfoNotify(f"Error Moving File: {e}")

    async def Rename_file(
        self, OldName: Path, NewName: Path
    ) -> Coroutine[None, None, str]:
        """
        Asynchronously renames a file while preserving its extension(s).

        Args:
            OldName (Path): The current file path.
            NewName (Path): The new file name or path.

        Returns:
            Coroutine[None, None, str]: A success or error message.

        """
        if NewName.suffix == "":
            if OldName.suffixes == 1:
                NewName = NewName.with_suffix(OldName.suffix)
            else:
                for suffix in OldName.suffixes:
                    NewName = NewName.with_suffix(NewName.suffix + suffix)

        Final: Path = OldName.parent / NewName
        if Final.exists():
            return AlreadyExist(Final.name, Final.parent)
        if OldName.exists():
            try:
                await asyncio.to_thread(OldName.rename, NewName)
                return f"[{need_theme()["foreground"]}]Renamed Successfully {OldName.name} -> {NewName.name}"
            except PermissionError:
                raise InfoNotify(f"Permission Denied")
            except Exception as e:

                raise InfoNotify(f"Error In Renaming.")
        elif not OldName.exists():
            raise InfoNotify(f"{OldName.name} Is Not Found.")
        elif NewName.exists():
            raise InfoNotify(f"Error {NewName.name} Is Aleady in {NewName.resolve().parent.name} Directory.")

    async def Copy_File(
        self, Source: Path, Destination: Path
    ) -> Coroutine[None, None, str]:
        """
        Asynchronously copies a file to the specified destination.

        Args:
            Source (Path): The path of the file to copy.
            Destination (Path): The target directory.

        Returns:
            Coroutine[None, None, str]: A success or error message.

        """
        Final = Destination / Source.name
        if Final.exists():
            return AlreadyExist(Final.name, Final.parent)
        elif Source.exists() and Destination.is_dir():
            try:
                await asyncio.to_thread(sl.copy2, Source, Final)
                return f"{Source.name} Copied Successfully to {Destination.name}."
            except PermissionError:
                raise InfoNotify("Permission Denied.")
            except Exception as e:

                raise InfoNotify(f"Error In Copying: {e}")
        elif Source.is_dir():
            return self.Copy_Folder(Source, Destination)
        elif not Source.exists():
            raise InfoNotify(f"{Source.name} Does Not Exist.")

    async def Create_File(self, Name: Path) -> Coroutine[None, None, str]:
        """
        Asynchronously creates a new file if it does not already exist.

        Args:
            Name (Path): The path of the file to be created.

        Returns:
            Coroutine[None, None, str]: A success or error message.

        """
        if Name.exists():
            return AlreadyExist(Name.name, Name.resolve().parent)
        try:
            if not Name.exists():
                await asyncio.to_thread(Name.touch)
                return f"[{need_theme()["foreground"]}]{Name.name} Is Created in {Name.resolve().parent} Directory"
            else:
                raise InfoNotify(f"{Name.name} Is Already in {Name.resolve().parent} Directory")
        except PermissionError:
            raise InfoNotify(f"Permission Denied")
        except Exception as e:

            raise InfoNotify(f"Error{e}")

    async def ShowContent_File(self, FileName: Path) -> Coroutine[None, None, str]:
        """
        Asynchronously displays the content of a file or lists folder contents.

        Args:
            FileName (Path): The path of the file or folder.

        Returns:
            Coroutine[None, None, str]: The file content in a formatted panel or
            an error message if the file/folder is not accessible.

        """
        if not FileName.exists():
            raise InfoNotify(f"{FileName.name} Not Found")

        try:
            if FileName.is_file():
                async with aiofiles.open(
                    FileName, mode="r", encoding="utf-8"
                ) as content:
                    file_content = await content.read()
                return Panel(Text(file_content, style="text"), title=FileName.name)
            elif FileName.is_dir():
                return self.ShowFolderContents(FileName)
            else:
                raise InfoNotify(f"Unsupported file type: {FileName}")
        except PermissionError:
            raise InfoNotify(f"Permission Denied: {FileName.name}")
        except Exception as e:

            raise InfoNotify(f"Error Reading {FileName.name}: {str(e)}")

    async def ClearContent_File(self, FileName: Path) -> Coroutine[None, None, str]:
        """
        Asynchronously clears the content of a file.

        Args:
            FileName (Path): The path of the file to be cleared.

        Returns:
            Coroutine[None, None, str]: A success message if cleared,
            or an error message if the file is not accessible.
        """

        if not FileName.exists():
            raise InfoNotify(f"{FileName.name} Not Found")

        if FileName.is_dir():
            raise InfoNotify(f"{FileName.name} is a Directory and cannot be cleared")

        try:
            async with aiofiles.open(FileName, mode="w") as _:
                pass
            return f"[{need_theme()["foreground"]}]{FileName.name} Content Cleared Successfully"
        except PermissionError:
            raise InfoNotify(f"Permission Denied for {FileName.name}")
        except Exception as e:

            raise InfoNotify(f"Error Clearing {FileName.name}: {str(e)}")

    async def Text_Finder_Directory(
        self, Text: str, Path: str = "."
    ) -> Coroutine[None, None, Table | str]:
        """
        Asynchronously searches for a text string in all files within a directory.

        Args:
            Text (str): The text string to search for.
            Path (str, optional): The directory path to search in. Defaults to the current directory.

        Returns:
            Coroutine[None, None, Table | str]: A table with matching file names and line numbers
            if matches are found, otherwise a "Text Not Found" message.
        """
        match_tables = Table(show_lines=True)
        match_tables.add_column("Line.no")
        match_tables.add_column("Filenmae")
        result = await Helper(Text, Path)

        if result:
            for file_path, line_num in result:
                match_tables.add_row(str(line_num), file_path)
            return match_tables
        else:
            return "Text Not Found"

    async def Text_Finder_File(
        self, Text: str, file_path: str
    ) -> Coroutine[None, None, Table]:
        """
        Asynchronously searches for a text string in a given file.

        Args:
            Text (str): The text string to search for.
            file_path (str): The path of the file to search in.

        Returns:
            Coroutine[None, None, Table]: A table displaying matching line numbers and text.
        """
        try:
            match_lines = Table(show_lines=True)
            match_lines.add_column("line no")
            match_lines.add_column("text")
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                line_num = 0
                async for line in f:
                    line_num += 1
                    if Text in line:
                        match_lines.add_row(str(line_num), Text)
            return match_lines
        except (UnicodeDecodeError, IOError):
            raise InfoNotify("Cant read at the moment or may be Binary file")

    async def search_items(
        self, query: str, path: str = ".", search_type: str = "both"
    ) -> Coroutine[None, None, Table | str]:

        matches_table = Table(show_lines=True)
        matches_table.add_column("Found")
        matches_table.add_column("Type")
        matches = []
        try:
            for root, dirs, files in os.walk(path):
                if search_type in ("folders", "both"):
                    for folder in dirs:
                        if folder.startswith(query):
                            matches.append(os.path.join(root, folder))
                            matches_table.add_row(
                                str(os.path.join(root, folder)), "Folder"
                            )

                if search_type in ("files", "both"):
                    for file in files:
                        if file.startswith(query):
                            matches.append(os.path.join(root, file))
                            matches_table.add_row(
                                str(os.path.join(root, folder)), "File"
                            )

            return matches_table
        except Exception as e:

            return []

    async def Create_Folder(self, Source: Path) -> Coroutine[None, None, str]:
        """
        Asynchronously creates a new folder if it does not already exist.

        Args:
            Source (Path): The directory path to be created.

        Returns:
            Coroutine[None, None, str]: A success message if created,
            or an error message if the folder already exists or cannot be created.
        """

        try:
            if Source.exists():
                return AlreadyExist(Source.name, Source.parent)
            await asyncio.to_thread(Source.mkdir, parents=True, exist_ok=False)
            return f"[{need_theme()["foreground"]}]{Source.name} Created Successfully at {Source.resolve().parent}"
        except PermissionError:
            raise InfoNotify(f"Permission Denied: Cannot Create {Source.name}")

        except FileExistsError:
            raise InfoNotify(f"{Source.name} Already Exists")
        except Exception as e:
            raise InfoNotify(f"Error Creating Folder {Source.name}: {str(e)}")

    async def Move_Folder(
        self, Source: Path, Destination: Path
    ) -> Coroutine[None, None, str]:
        """
        Asynchronously moves a folder or file to the specified destination.

        Args:
            Source (Path): The path of the folder or file to move.
            Destination (Path): The target directory.

        Returns:
            Coroutine[None, None, str]: A success message if moved,
            or an error message if the operation fails.
        """

        try:
            Final = Destination / Source.name

            if Final.exists():
                raise InfoNotify(f"{Final.name} Already Exists in {Final.resolve().parent}")

            if not Source.exists():
                raise InfoNotify(f"{Source.name} Not Found")
            if not Destination.exists():
                raise InfoNotify(f"{Destination.name} Directory Not Found")
            if not Destination.is_dir():
                raise InfoNotify(f"{Destination.name} Is Not a Directory")

            await asyncio.to_thread(sl.move, Source, Destination)
            return f"[{need_theme()["foreground"]}]{Source.name} Moved Successfully to {Destination.resolve().name}"

        except PermissionError:
            raise InfoNotify("Permission Denied")
        except Exception as e:
            raise InfoNotify(f"Error Moving File or Directory: {str(e)}")

    async def Copy_Folder(
        self, Source: Path, Destination: Path
    ) -> Coroutine[None, None, str]:
        """
        Asynchronously copies a folder or file to the specified destination.

        Args:
            Source (Path): The path of the folder or file to copy.
            Destination (Path): The target directory.

        Returns:
            Coroutine[None, None, str]: A success message if copied,
            or an error message if the operation fails.
        """

        try:
            Final = Destination / Source.name

            if Final.exists():
                raise InfoNotify(f"{Final.name} Already Exists in {Final.resolve().parent}")
            if not Source.exists():
                raise InfoNotify(f"{Source.name} Does Not Exist")
            if not Destination.exists():
                raise InfoNotify(f"{Destination.name} Directory Not Found")
            if not Destination.is_dir():
                raise InfoNotify(f"{Destination.name} Is Not a Directory")

            if Source.is_dir():
                await asyncio.to_thread(sl.copytree, Source, Final, dirs_exist_ok=True)
                return f"[{need_theme()["foreground"]}]{Source.name} Directory Copied Successfully to {Destination.resolve().name}"

            # Handle copying file
            elif Source.is_file():
                await asyncio.to_thread(sl.copy2, Source, Final)
                return f"[{need_theme()["foreground"]}]{Source.name} File Copied Successfully to {Destination.resolve().name}"

            else:
                raise InfoNotify(f"Unsupported File Type: {Source.name}")

        except PermissionError:
            raise InfoNotify("Permission Denied")
        except Exception as e:
            raise InfoNotify(f"Error in Copying: {str(e)}")

    async def Delete_Folder(self, FolderName: Path) -> Coroutine[None, None, str]:
        """
        Asynchronously deletes a folder and its contents.

        Args:
            FolderName (Path): The directory path to be deleted.

        Returns:
            Coroutine[None, None, str]: A success message if deleted,
            or an error message if the folder does not exist or cannot be deleted.

        """

        if not FolderName.exists():
            raise InfoNotify(f"{FolderName.name} Not Found.")

        try:
            if FolderName.is_dir():
                await asyncio.to_thread(sl.rmtree, FolderName)
            else:
                await asyncio.to_thread(FolderName.unlink)
            return f"[{need_theme()["foreground"]}]{FolderName.name} Deleted Successfully."
        except PermissionError:
            raise InfoNotify(f"Permission Denied for {FolderName.name}")
        except Exception as e:
            raise InfoNotify(f"Error Deleting {FolderName.name}: {str(e)}")


async def Helper(Text: str, Path: str) -> list[str]:
    """
    Asynchronously searches for a text string in all files within a directory.

    Args:
        Text (str): The text string to search for.
        Path (str): The directory path to search in.

    Returns:
        list[str]: A list of matching file paths with line numbers.

    Raises:
        Exception: If an unexpected error occurs during file traversal or search.
    """
    matching_files = []
    for root, dirs, files in os.walk(Path):
        tasks = [
            search_in_file(Text, os.path.join(root, file), matching_files)
            for file in files
        ]
        await asyncio.gather(*tasks)
    return matching_files


async def search_in_file(Text: str, file_path: str, matching_files: list) -> None:
    """
    Asynchronously searches for a text string in a given file.

    Args:
        Text (str): The text string to search for.
        file_path (str): The path of the file to search in.
        matching_files (list): A list to store tuples of (file path, line number)
                               where matches are found.

    Returns:
        None: Updates the matching_files list with search results.

    Raises:
        UnicodeDecodeError, IOError: If the file cannot be read (e.g., encoding issues or I/O errors).
    """
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            line_num = 0
            async for line in f:
                line_num += 1
                if Text in line:
                    matching_files.append((file_path, line_num))
    except (UnicodeDecodeError, IOError):
        pass
