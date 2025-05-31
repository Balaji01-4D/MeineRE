import asyncio
import gzip
import os
import shutil
import tarfile
import zipfile
from pathlib import Path

import py7zr
from rich.panel import Panel
from rich.table import Table

from meine.exceptions import InfoNotify


class Zip:

    async def Compress(self, Source: Path, format: str = "zip") -> str:
        try:
            if not Source.exists():
                return f"{Source.name} Is Not Found."

            if format in {"zip", "z"}:
                await asyncio.to_thread(self._compress_zip, Source)
                return f"{Source.name} Compressed Successfully as zip."
            elif format == "tar":
                await asyncio.to_thread(self._compress_tar, Source)
                return f"{Source.name} Compressed Successfully as tar."
            elif format == "gz":
                await asyncio.to_thread(self._compress_gz, Source)
                return f"{Source.name} Compressed Successfully as gz."
            elif format == "7z":
                await asyncio.to_thread(self._compress_7z, Source)
                return f"{Source.name} Compressed Successfully as 7z."
            else:
                return f"Unsupported compression format: {format}. Please use zip, tar, gz, or 7z."

        except PermissionError:
            raise InfoNotify("Permission Denied")
        except Exception as e:
            raise InfoNotify(f"Error in compressing {Source.name}: {str(e)}")

    # Helper methods for each compression format
    def _compress_zip(self, Source: Path):
        with zipfile.ZipFile(str(Source) + ".zip", "w", zipfile.ZIP_DEFLATED) as zipf:
            if Source.is_dir():
                for foldername, subfolders, filenames in os.walk(Source):
                    for filename in filenames:
                        file_path = Path(foldername) / filename
                        zipf.write(
                            file_path, arcname=file_path.relative_to(Source.parent)
                        )
            else:
                zipf.write(Source, arcname=Source.name)

    def _compress_tar(self, Source: Path):
        if Source.is_dir():
            with tarfile.open(str(Source) + ".tar.gz", "w:gz") as tarf:
                tarf.add(Source, arcname=Source.name)
        else:
            with tarfile.open(str(Source) + ".tar.gz", "w:gz") as tarf:
                tarf.add(Source, arcname=Source.name)

    def _compress_gz(self, Source: Path):
        if Source.is_dir():
            return "Cannot compress directories as .gz, use another format like .tar or .zip."
        else:
            with open(Source, "rb") as f_in:
                with gzip.open(str(Source) + ".gz", "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

    def _compress_7z(self, Source: Path):
        import py7zr

        if Source.is_dir():
            with py7zr.SevenZipFile(str(Source) + ".7z", mode="w") as zf:
                zf.writeall(Source, arcname=Source.name)
        else:
            with py7zr.SevenZipFile(str(Source) + ".7z", mode="w") as zf:
                zf.write(Source, arcname=Source.name)

    async def Extract(self, Source: Path) -> str:
        if not Source.exists():
            return f"{Source.name} Not Found."

        try:
            StrSource = str(Source)

            # Handle '.zip' files
            if StrSource.endswith(".zip"):
                await asyncio.to_thread(self._extract_zip, Source)
                return f"{Source.stem} Extracted Successfully as zip."

            # Handle '.tar' and '.tar.gz' files
            elif StrSource.endswith(".tar") or StrSource.endswith(".tar.gz"):
                await asyncio.to_thread(self._extract_tar, Source)
                return f"{Source.stem} Extracted Successfully as tar."

            # Handle '.gz' files (single file extraction)
            elif StrSource.endswith(".gz"):
                await asyncio.to_thread(self._extract_gz, Source)
                return f"{Source.stem} Extracted Successfully as gz."

            # Handle '.7z' files
            elif StrSource.endswith(".7z"):
                await asyncio.to_thread(self._extract_7z, Source)
                return f"{Source.stem} Extracted Successfully as 7z."

            else:
                return f"Unsupported file format: {Source.suffix}. Please use .zip, .tar, .gz, or .7z for extraction."

        except PermissionError:
            raise InfoNotify("Permission Denied")
        except Exception as e:
            raise InfoNotify(f"Error In Extracting {Source.name}: {str(e)}")

    # Helper methods for each extraction format
    def _extract_zip(self, Source: Path):
        with zipfile.ZipFile(Source, "r") as zipf:
            zipf.extractall(Source.parent)

    def _extract_tar(self, Source: Path):
        with tarfile.open(Source, "r:gz") as tarf:
            tarf.extractall(Source.parent)

    def _extract_gz(self, Source: Path):
        with gzip.open(Source, "rb") as gz_file:
            with open(Source.stem, "wb") as out_file:
                shutil.copyfileobj(gz_file, out_file)

    def _extract_7z(self, Source: Path):
        with py7zr.SevenZipFile(Source, mode="r") as zf:
            zf.extractall(path=Source.parent)

    async def list_contents(self, archive_file: Path) -> str:
        try:
            # Check if file exists
            if not archive_file.exists():
                return f"{archive_file.name} not found."

            # Initialize a table to display contents
            content_table = Table(
                show_lines=True, title="[accent]ARCHIVE CONTENT", border_style="borders"
            )
            content_table.add_column("NAME", style="accent")
            content_table.add_column("TYPE")
            content_table.add_column("SIZE", style="accent")

            # Handle based on file extension (zip, tar, 7z, etc.)
            if archive_file.suffix == ".zip":
                return await self._list_zip_contents(archive_file, content_table)

            elif archive_file.suffix == ".tar" or archive_file.suffix == ".gz":
                return await self._list_tar_contents(archive_file, content_table)

            elif archive_file.suffix == ".7z":
                return await self._list_7z_contents(archive_file, content_table)

            else:
                return f"{archive_file.name} is not a valid archive file format."

        except PermissionError:
            raise InfoNotify("Permission Denied")
        except Exception as e:
            raise InfoNotify(f"Error occurred: {str(e)}")

    # Function for handling .zip files
    async def _list_zip_contents(self, zip_file: Path, content_table: Table) -> str:
        try:
            with zipfile.ZipFile(zip_file, "r") as zf:
                for file in zf.infolist():
                    file_type = "Folder" if file.is_dir() else "File"
                    content_table.add_row(
                        file.filename, file_type, SizeHelper(file.file_size)
                    )
            return Panel(content_table, expand=False, border_style="borders")
        except Exception as e:
            return f"Error in reading {zip_file.name}: {str(e)}"

    # Function for handling .tar and .gz files
    async def _list_tar_contents(self, tar_file: Path, content_table: Table) -> str:
        try:
            with tarfile.open(tar_file, "r") as tf:
                for file in tf.getnames():
                    file_info = tf.getmember(file)
                    file_type = "Folder" if file_info.isdir() else "File"
                    content_table.add_row(file, file_type, SizeHelper(file_info.size))
            return Panel(content_table, expand=False, border_style="borders")
        except Exception as e:
            return f"Error in reading {tar_file.name}: {str(e)}"

    # Function for handling .7z files
    async def _list_7z_contents(self, sevenz_file: Path, content_table: Table) -> str:
        try:
            with py7zr.SevenZipFile(sevenz_file, mode="r") as zf:
                for file in zf.getnames():
                    # Since py7zr doesn't expose size directly, we use 'None' for now
                    content_table.add_row(file, "File", "Size info unavailable")
            return Panel(content_table, expand=False, border_style="borders")
        except Exception as e:
            return f"Error in reading {sevenz_file.name}: {str(e)}"


def SizeHelper(size: int) -> str:
    if size >= 1024**2:
        return f"{size / (1024**2):.2f} MB"
    elif size >= 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size} bytes"
