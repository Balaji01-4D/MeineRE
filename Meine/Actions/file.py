import asyncio
import os
import shutil as sl
from pathlib import Path
from typing import Coroutine

import aiofiles
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from Meine.exceptions import InfoNotify
from Meine.logger_config import log_time, logger

from .Myrequest import AlreadyExist


class File:

    @log_time
    async def Delete_File(self, FileName: Path) -> Coroutine[None, None, str]:
        logger.info(f"{self.Delete_File.__name__} executing")
        if FileName.is_dir():
            return self.Delete_Folder(FileName)
        if FileName.is_file():
            try:
                await asyncio.to_thread(FileName.chmod, 0o744)
                await asyncio.to_thread(FileName.unlink)
                return f"[success] {FileName.name} Deleted Successfully."
            except FileNotFoundError:
                InfoNotify(f"File Not found")

            except PermissionError:
                InfoNotify(f"Permission denied")
            except Exception as e:
                logger.error(f"{e} Function: {self.Delete_File.__name__}")
                return f"[error] Error In Deleting {FileName.name}: {e}"
        else:
            return f"[error] {FileName.name} Not Found."

    @log_time
    async def Move_File(
        self, Source: Path, Destination: Path
    ) -> Coroutine[None, None, str]:
        Final = Destination / Source.name

        if Final.exists():
            return AlreadyExist(Final.name, Final.parent)

        if not Source.exists():
            return f"[error] {Source.name} Not Found."
        if not Destination.exists() or not Destination.is_dir():
            return f"[error] {Destination.name} Is Not a Valid Directory."
        try:
            await asyncio.to_thread(sl.move, Source, Final)
            return f"[success] {Source.name} Moved Successfully to {Destination.name}."
        except PermissionError:
            return "[error] Permission Denied."
        except Exception as e:
            logger.error(f"{e} Function: {self.Move_File.__name__}")
            return f"[error] Error Moving File: {e}"

    @log_time
    async def Rename_file(
        self, OldName: Path, NewName: Path
    ) -> Coroutine[None, None, str]:
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
                return f"[success]Renamed Successfully {OldName.name} -> {NewName.name}"
            except PermissionError:
                return f"[error]Permission Denied"
            except Exception as e:
                logger.error(f"{e} Function: {self.Rename_file.__name__}")
                return f"[error]Error In Renaming."
        elif not OldName.exists():
            return f"[error]{OldName.name} Is Not Found."
        elif NewName.exists():
            return f"[error]Error {NewName.name} Is Aleady in {NewName.resolve().parent.name} Directory."

    @log_time
    async def Copy_File(
        self, Source: Path, Destination: Path
    ) -> Coroutine[None, None, str]:
        Final = Destination / Source.name
        if Final.exists():
            return AlreadyExist(Final.name, Final.parent)
        elif Source.exists() and Destination.is_dir():
            try:
                await asyncio.to_thread(sl.copy2, Source, Final)
                return f"{Source.name} Copied Successfully to {Destination.name}."
            except PermissionError:
                return "[error] Permission Denied."
            except Exception as e:
                logger.error(f"{e} Function: {self.Copy_File.__name__}")
                return f"[error] Error In Copying: {e}"
        elif Source.is_dir():
            return self.Copy_Folder(Source, Destination)
        elif not Source.exists():
            return f"[error] {Source.name} Does Not Exist."

    @log_time
    async def Create_File(self, Name: Path) -> Coroutine[None, None, str]:
        if Name.exists():
            return AlreadyExist(Name.name, Name.resolve().parent)
        try:
            if not Name.exists():
                await asyncio.to_thread(Name.touch)
                return f"[success]{Name.name} Is Created in {Name.resolve().parent} Directory"
            else:
                return f"[error]{Name.name} Is Already in {Name.resolve().parent} Directory"
        except PermissionError:
            return f"[error]Permission Denied"
        except Exception as e:
            logger.error(f"{e} Function: {self.Create_File.__name__}")
            return f"[error]Error{e}"

    @log_time
    async def ShowContent_File(self, FileName: Path) -> Coroutine[None, None, str]:
        """
        Displays the content of a file or the structure of a directory.

        :param FileName: Path to the file or folder.
        :return: A string formatted with rich.panel.Panel.
        """
        if not FileName.exists():
            return f"[error]{FileName.name} Not Found"

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
                return f"[error]Unsupported file type: {FileName}"
        except PermissionError:
            return f"[error]Permission Denied: {FileName.name}"
        except Exception as e:
            logger.error(f"{e} Function: {self.ShowContent_File.__name__}")
            return f"[error]Error Reading {FileName.name}: {str(e)}"

    @log_time
    async def ClearContent_File(self, FileName: Path) -> Coroutine[None, None, str]:
        """
        Clears the content of a file. Handles errors gracefully.

        :param FileName: Path to the file to clear.
        :return: A success or error message.
        """
        if not FileName.exists():
            return f"[error]{FileName.name} Not Found"

        if FileName.is_dir():
            return f"[error]{FileName.name} is a Directory and cannot be cleared"

        try:
            async with aiofiles.open(FileName, mode="w") as _:
                pass
            return f"[success]{FileName.name} Content Cleared Successfully"
        except PermissionError:
            return f"[error]Permission Denied for {FileName.name}"
        except Exception as e:
            logger.error(f"{e} Function: {self.ClearContent_File.__name__}")
            return f"[error]Error Clearing {FileName.name}: {str(e)}"

    @log_time
    async def Text_Finder_Directory(
        self, Text: str, Path: str = "."
    ) -> Coroutine[None, None, Table | str]:
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

    @log_time
    async def Text_Finder_File(
        self, Text: str, file_path: str
    ) -> Coroutine[None, None, Table]:
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

    @log_time
    async def search_items(
        self, query: str, path: str = ".", search_type: str = "both"
    ) -> Coroutine[None, None, Table | str]:
        """
        Search for files or folders matching a query in the given path.

        :param query: The string to search for. Matches items starting with this string.
        :param path: The directory to search in (default is the current directory).
        :param search_type: What to search for: 'files', 'folders', or 'both' (default is 'both').
        :return: A list of matching file or folder paths.
        """
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
            logger.error(f"{e} Function: {self.search_items.__name__}")
            print(f"Error occurred during search: {str(e)}")
            return []

    @log_time
    async def Create_Folder(self, Source: Path) -> Coroutine[None, None, str]:
        """
        Creates a directory at the specified Source path.

        :param Source: The path where the directory should be created.
        :return: A success or error message.
        """
        try:
            # Check if the directory already exists
            if Source.exists():
                return (
                    f"[error]{Source.name} Already Exists in {Source.resolve().parent}"
                )

            # Attempt to create the directory
            await asyncio.to_thread(Source.mkdir, parents=True, exist_ok=False)
            return f"[success]{Source.name} Created Successfully at {Source.resolve().parent}"

        except PermissionError:
            return f"[error]Permission Denied: Cannot Create {Source.name}"

        except FileExistsError:
            return f"[error]{Source.name} Already Exists"  # Additional safeguard

        except Exception as e:
            logger.error(f"{e} Function: {self.Create_Folder.__name__}")

            return f"[error]Error Creating Folder {Source.name}: {str(e)}"

    @log_time
    async def Move_Folder(
        self, Source: Path, Destination: Path
    ) -> Coroutine[None, None, str]:
        """
        Moves a file or directory from Source to Destination.

        :param Source: The source path to move.
        :param Destination: The destination directory.
        :return: A success or error message.
        """
        try:
            # Resolve the final destination
            Final = Destination / Source.name

            # Check if the destination already contains a file/folder with the same name
            if Final.exists():
                return f"[error]{Final.name} Already Exists in {Final.resolve().parent}"

            # Check for invalid paths
            if not Source.exists():
                return f"[error]{Source.name} Not Found"
            if not Destination.exists():
                return f"[error]{Destination.name} Directory Not Found"
            if not Destination.is_dir():
                return f"[error]{Destination.name} Is Not a Directory"

            # Perform the move operation
            await asyncio.to_thread(sl.move, Source, Destination)
            return f"[success]{Source.name} Moved Successfully to {Destination.resolve().name}"

        except PermissionError:
            return "[error]Permission Denied"
        except Exception as e:
            logger.error(f"{e} Function: {self.Move_Folder.__name__}")

            return f"[error]Error Moving File or Directory: {str(e)}"

    @log_time
    async def Copy_Folder(
        self, Source: Path, Destination: Path
    ) -> Coroutine[None, None, str]:
        """
        Copies a file or directory from Source to Destination.

        :param Source: The source path to copy.
        :param Destination: The destination directory.
        :return: A success or error message.
        """
        try:
            Final = Destination / Source.name

            if Final.exists():
                return f"[error]{Final.name} Already Exists in {Final.resolve().parent}"
            if not Source.exists():
                return f"[error]{Source.name} Does Not Exist"
            if not Destination.exists():
                return f"[error]{Destination.name} Directory Not Found"
            if not Destination.is_dir():
                return f"[error]{Destination.name} Is Not a Directory"

            if Source.is_dir():
                await asyncio.to_thread(sl.copytree, Source, Final, dirs_exist_ok=True)
                return f"[success]{Source.name} Directory Copied Successfully to {Destination.resolve().name}"

            # Handle copying file
            elif Source.is_file():
                await asyncio.to_thread(sl.copy2, Source, Final)
                return f"[success]{Source.name} File Copied Successfully to {Destination.resolve().name}"

            else:
                return f"[error]Unsupported File Type: {Source.name}"

        except PermissionError:
            return "[error]Permission Denied"
        except Exception as e:
            logger.error(f"{e} Function: {self.Copy_Folder.__name__}")

            return f"[error]Error in Copying: {str(e)}"

    @log_time
    async def Delete_Folder(self, FolderName: Path) -> Coroutine[None, None, str]:
        """
        Deletes a folder or file asynchronously.

        :param FolderName: Path to the folder or file to delete.
        :return: A success or error message.
        """
        if not FolderName.exists():
            return f"[error]{FolderName.name} Not Found."

        try:
            # Use asyncio.to_thread for blocking I/O operations
            if FolderName.is_dir():
                await asyncio.to_thread(sl.rmtree, FolderName)
            else:
                await asyncio.to_thread(FolderName.unlink)
            return f"[success]{FolderName.name} Deleted Successfully."
        except PermissionError:
            return f"[error]Permission Denied for {FolderName.name}"
        except Exception as e:
            logger.error(f"{e} Function: {self.Delete_Folder.__name__}")

            return f"[error]Error Deleting {FolderName.name}: {str(e)}"


async def Helper(Text: str, Path: str) -> list[str]:
    matching_files = []
    for root, dirs, files in os.walk(Path):
        # Create a list of tasks to process files concurrently
        tasks = [
            search_in_file(Text, os.path.join(root, file), matching_files)
            for file in files
        ]
        # Await the completion of all tasks
        await asyncio.gather(*tasks)
    return matching_files


async def search_in_file(Text: str, file_path: str, matching_files: list):
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            line_num = 0
            async for line in f:
                line_num += 1
                if Text in line:
                    matching_files.append((file_path, line_num))
    except (UnicodeDecodeError, IOError):
        pass
