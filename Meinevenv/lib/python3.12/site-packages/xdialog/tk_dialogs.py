from .constants import *

from tkinter import messagebox
from tkinter import filedialog

def open_file(title, filetypes, multiple=False):
    if multiple:
        return filedialog.askopenfilenames(title=title, filetypes=filetypes)
    else:
        return filedialog.askopenfilename(title=title) or ''

def save_file(title, filetypes):
    return filedialog.asksaveasfilename(title=title, filetypes=filetypes) or ''

def directory(title):
    return filedialog.askdirectory(mustexist=True) or ''

info = messagebox.showinfo
warning = messagebox.showwarning
error = messagebox.showerror

def yesno(title, message):
    if messagebox.askyesno(title, message):
        return YES
    else:
        return NO

def yesnocancel(title, message):
    r = messagebox.askyesnocancel(title, message)
    if r is None:
        return CANCEL
    elif r:
        return YES
    else:
        return NO

def retrycancel(title, message):
    if messagebox.askretrycancel(title, message):
        return RETRY
    else:
        return CANCEL

def okcancel(title, message):
    if messagebox.askokcancel(title, message):
        return OK
    else:
        return CANCEL
