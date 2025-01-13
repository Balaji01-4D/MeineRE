from MeineAI.Actions import File
f = File()
import asyncio
from rich.table import Table
import os
import aiofiles

async def Text_Finder_Directory(self, Text: str, Path: str = '.') -> None:
    match_tables = Table(show_lines=True)
    match_tables.add_column('Line.no')
    match_tables.add_column('Filenmae')
    result = await Helper(Text, Path)
    
    if result:
        for file_path, line_num in result:
            match_tables.add_row(str(line_num),file_path.replace('./', os.getcwd() + '/'))
        return match_tables
    else:
        return ("Text Not Found")
async def Helper(Text: str, Path: str) -> list[str]:
        matching_files = []
        for root, dirs, files in os.walk(Path):
            # Create a list of tasks to process files concurrently
            tasks = [search_in_file(Text, os.path.join(root, file), matching_files) for file in files]
            # Await the completion of all tasks
            await asyncio.gather(*tasks)
        return matching_files

async def search_in_file(Text: str, file_path: str, matching_files: list):
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            line_num = 0
            async for line in f:
                line_num += 1
                if Text in line:
                    matching_files.append((file_path, line_num))
        print(matching_files)
    except (UnicodeDecodeError, IOError):
        pass
        

from rich.console import Console
con = Console()
result = asyncio.run(Text_Finder_Directory(1,"RaiseNotify"))
con.print(result)