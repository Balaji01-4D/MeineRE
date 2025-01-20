#!/usr/bin/env python3

import subprocess

from .constants import *

def osascript(*code: str):
    proc = subprocess.Popen(
        ["osascript", "-e", " ".join(code)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    )
    stdout, stderr = proc.communicate()

    return (proc.returncode, stdout.decode('utf-8'), stderr.decode('utf-8'))

def quote(text: str):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'

def dialog(title, message, icon, buttons=["OK"]):
    script = [
        'display dialog', quote(message),
        'with icon', icon,
        'buttons', "{" + ",".join(quote(btn) for btn in buttons) + "}",
    ]
    if title: script.append('with title ' + quote(title))

    code, out, err = osascript(*script)
    if code: return ''
    else: return out[out.index(":")+1:].strip("\r\n")

def open_file(title, filetypes, multiple=False):
    script = ['choose file']
    if title: script.append('with prompt ' + quote(title))
    if filetypes:
        oftype = []
        for _, exts in filetypes:
            for ext in exts.split():
                if ext == "*": break
                if ext[:2] == "*.": oftype.append(quote(ext[2:]))
        else:
            if oftype: script.append("of type {" + ",".join(oftype) + "}")
    
    if multiple:
        script.append("multiple selections allowed true")
        code, out, err = osascript(f'set ps to ({" ".join(script)})\rrepeat with p in ps\r log (POSIX path of p)\rend repeat')
        if code: return []

        return err.strip("\r\n").splitlines()
    else:
        code, out, err = osascript(f'POSIX path of ({" ".join(script)})')
        if code: return ''

        return out.strip("\r\n")

def save_file(title, filetypes):
    script = ['choose file name']
    if title: script.append('with prompt ' + quote(title))
    if filetypes:
        for filetype, exts in filetypes:
            for ext in exts.split():
                if ext == "*": continue
                if ext[:2] == "*.":
                    script.append(f'default name "{filetype}.{ext[2:]}"') 
                    break

    code, out, err = osascript(f'POSIX path of ({" ".join(script)})')
    if code: return ''

    return out.strip("\r\n")

def directory(title):
    script = ['choose folder']
    if title: script.append('with prompt ' + quote(title))

    code, out, err = osascript(f'POSIX path of ({" ".join(script)})')
    if code: return ''

    return out.strip("\r\n")

def info(title, message):
    dialog(title, message, "note")

def warning(title, message):
    dialog(title, message, "caution")

def error(title, message):
    dialog(title, message, "stop")

def yesno(title, message):
    out = dialog(title, message, "note", ["No", "Yes"])
    if not out or out == "No": return NO
    elif out == "Yes": return YES

def yesnocancel(title, message):
    out = dialog(title, message, "note", ["Cancel", "No", "Yes"])
    if not out or out == "Cancel": return CANCEL
    elif out == "No": return NO
    elif out == "Yes": return YES

def retrycancel(title, message):
    out = dialog(title, message, "note", ["Cancel", "Retry"])
    if not out or out == "Cancel": return CANCEL
    elif out == "Retry": return RETRY

def okcancel(title, message):
    out = dialog(title, message, "note", ["Cancel", "OK"])
    if not out or out == "Cancel": return CANCEL
    elif out == "OK": return OK
