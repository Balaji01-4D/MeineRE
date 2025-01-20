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

def zenity(typ, filetypes=None, **kwargs) -> Tuple[int, str]:
    # Build args based on keywords
    args = ['zenity', '--'+typ]
    for k, v in kwargs.items():
        if v is True:
            args.append(f'--{k.replace("_", "-").strip("-")}')
        elif isinstance(v, str):
            cv = clean(v) if k != "title" else v
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
    # Zenity is strange and will let you select folders for some reason in some cases. So we filter those out.
    if multiple:
        files = zenity('file-selection', title=title, filetypes=filetypes, multiple=True, separator="\n")[1].splitlines()
        return list(filter(isfile, files))
    else:
        file = zenity('file-selection', title=title, filetypes=filetypes)[1]
        if file and isfile(file):
            return file
        else:
            return ''

def save_file(title, filetypes):
    return zenity('file-selection', title=title, filetypes=filetypes, save=True)[1]

def directory(title):
    return zenity("file-selection", title=title, directory=True)[1]

def info(title, message):
    zenity("info", title=title, text=message)

def warning(title, message):
    zenity("warning", title=title, text=message)

def error(title, message):
    zenity("error", title=title, text=message)

def yesno(title, message):
    return zenity("question", title=title, text=message)[0]

def yesnocancel(title, message):
    r = zenity(
        "question",
        title=title,
        text=message,
        extra_button="No",
        cancel_label="Cancel"
    )

    if r[1]:
        return NO
    elif r[0]:
        return CANCEL
    else:
        return YES

def retrycancel(title, message):
    r = zenity(
        "question",
        title=(title or ""),
        text=message,
        ok_label="Retry",
        cancel_label="Cancel"
    )[0]

    if r:
        return CANCEL
    else:
        return RETRY

def okcancel(title, message):
    r = zenity(
        "question",
        title=title,
        text=message,
        ok_label="Ok",
        cancel_label="Cancel"
    )[0]

    if r:
        return CANCEL
    else:
        return OK