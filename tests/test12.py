    
from pathlib import Path
import asyncio
async def Rename_file( OldName: Path, NewName: Path) -> str:
    if NewName.suffix == "":
        if (OldName.suffixes == 1):
            NewName = NewName.with_suffix(OldName.suffix)
        else:
            for suffix in OldName.suffixes:
                NewName = NewName.with_suffix(NewName.suffix + suffix)                
            
    Final: Path = OldName.parent/NewName
    if (Final.exists()):
        return 'already'
    if (OldName.exists()):
        try :
            await asyncio.to_thread(OldName.rename,NewName)
            return(f"[success]Renamed Successfully {OldName.name} -> {NewName.name}")
        except PermissionError:
            return(f"[error]Permission Denied")
        except Exception as e:
            return(f"[error]Error In Renaming.")
    elif (not OldName.exists()):
        return(f"[error]{OldName.name} Is Not Found.")
    elif (NewName.exists()):
        return(f"[error]Error {NewName.name} Is Aleady in {NewName.resolve().parent.name} Directory.")

print(Path.cwd())
result = asyncio.run(Rename_file(Path('test.py'),Path('test12')))
print(result)