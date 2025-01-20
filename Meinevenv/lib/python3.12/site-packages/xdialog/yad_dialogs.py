import subprocess
from os.path import isfile
from typing import Tuple

from .constants import *

def clean(txt: str):
    return txt\
        .replace("\\", "\\\\")\
        .replace("$", "\\$")\
        .replace("!", "\\!")\
        .replace("*", "\\*")\
        .replace("?", "\\?")\
        .replace("&", "&amp;")\
        .replace("|", "&#124;")\
        .replace("<", "&lt;")\
        .replace(">", "&gt;")\
        .replace("(", "\\(")\
        .replace(")", "\\)")\
        .replace("[", "\\[")\
        .replace("]", "\\]")\
        .replace("{", "\\{")\
        .replace("}", "\\}")\

# TODO: Make the boxes bigger
# TODO: Make the icons correct

def yad(typ, filetypes=None, **kwargs) -> Tuple[int, str]:
    # Build args based on keywords
    args = ['yad', '--'+typ]
    for k, v in kwargs.items():
        vv = v
        if not isinstance(v, list):
            vv = [v]

        for vvv in vv:
            if vvv is True:
                args.append(f'--{k.replace("_", "-").strip("-")}')
            elif isinstance(vvv, str):
                cv = clean(vvv) if k != "title" else vvv
                args.append(f'--{k.replace("_", "-").strip("-")}={cv}')

    # Build filetypes specially if specified
    if filetypes:
        for name, globs in filetypes:
            if name:
                globlist = globs.split()
                args.append(f'--file-filter={name.replace("|", "")} ({", ".join(t for t in globlist)})|{globs}')

    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        shell=False
    )
    stdout, _ = proc.communicate()

    return (proc.returncode, stdout.decode('utf-8').strip())


def open_file(title, filetypes, multiple=False):
    # Yad is strange and will let you select folders for some reason in some cases. So we filter those out.
    if multiple:
        files = yad('file', title=(title or ""), filetypes=filetypes, multiple=True, separator="\n", width="800", height="600")[1].splitlines()
        return list(filter(isfile, files))
    else:
        file = yad('file', title=(title or ""), filetypes=filetypes, width="800", height="600")[1]
        if file and isfile(file):
            return file
        else:
            return ''

def save_file(title, filetypes):
    return yad('file', title=(title or ""), filetypes=filetypes, save=True, width="800", height="600")[1]

def directory(title):
    return yad("file", title=(title or ""), directory=True, width="800", height="600")[1]

def info(title, message):
    yad(
        "info",
        title=(title or ""),
        text=message,
        image="dialog-information",
        window_icon="dialog-information",
        width="350",
        button=f"OK:{OK}"
    )

def warning(title, message):
    yad(
        "warning",
        title=(title or ""),
        text=message,
        image="dialog-warning",
        window_icon="dialog-warning",
        width="350",
        button=f"OK:{OK}"
    )

def error(title, message):
    yad(
        "error",
        title=(title or ""),
        text=message,
        image="dialog-error",
        window_icon="dialog-error",
        width="350",
        button=f"OK:{OK}"
    )

def yesno(title, message):
    r = yad(
        "question",
        title=(title or ""),
        text=message,
        image="dialog-question",
        window_icon="dialog-question",
        width="350",
        button=[f"No:{NO}", f"Yes:{YES}"]
    )[0]
    return NO if r > 128 or r < 0 else r

def yesnocancel(title, message):
    r = yad(
        "question",
        title=(title or ""),
        text=message,
        image="dialog-question",
        window_icon="dialog-question",
        width="350",
        button=[f"Cancel:{CANCEL}", f"No:{NO}", f"Yes:{YES}"]
    )[0]
    return CANCEL if r > 128 or r < 0 else r

def retrycancel(title, message):
    r = yad(
        "question",
        title=(title or ""),
        text=message,
        image="dialog-question",
        window_icon="dialog-question",
        width="350",
        button=[f"Cancel:{CANCEL}", f"Retry:{RETRY}"]
    )[0]
    return CANCEL if r > 128 or r < 0 else r

def okcancel(title, message):
    r = yad(
        "question",
        title=(title or ""),
        text=message,
        image="dialog-question",
        window_icon="dialog-question",
        width="350",
        button=[f"Cancel:{CANCEL}", f"OK:{OK}"]
    )[0]
    return CANCEL if r > 128 or r < 0 else r