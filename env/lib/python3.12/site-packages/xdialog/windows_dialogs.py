import ctypes
import atexit

from .constants import *
from .windows_structs import *

# dlls
user32 = ctypes.windll.user32
comdlg32 = ctypes.windll.comdlg32
shell32 = ctypes.windll.shell32
ole32 = ctypes.oledll.ole32

BUFFER_SIZE = 8192


def split_null_list(strp):
    p = ctypes.cast(strp, ctypes.c_wchar_p)
    v = p.value
    while v:
        yield v
        loc = ctypes.cast(p, ctypes.c_void_p).value + (len(v)*2+2)
        p = ctypes.cast(loc, ctypes.c_wchar_p)
        v = p.value


def open_file(title, filetypes, multiple=False):
    file = ctypes.create_unicode_buffer(BUFFER_SIZE)
    pfile = ctypes.cast(file, ctypes.c_wchar_p)

    # Default options
    opts = tagOFNW(
        lStructSize=ctypes.sizeof(tagOFNW),

        lpstrFile=pfile,
        nMaxFile=BUFFER_SIZE,

        lpstrTitle=title,
        Flags=0x00081808 + (0x200 if multiple else 0)
    )

    # Filetypes
    if filetypes:
        out = []
        for s, t in filetypes:
            out.append(f'{s} ({t})\0{";".join(t.split())}\0')
        
        buf = ctypes.create_unicode_buffer(''.join(out)+'\0')

        opts.lpstrFilter = LPCWSTR(ctypes.addressof(buf))
        opts.lpstrDefExt = LPCWSTR(ctypes.addressof(buf))
    
    # Call file dialog
    ok = comdlg32.GetOpenFileNameW(ctypes.byref(opts))

    # Return data
    if multiple:
        if ok:
            # Windows splits the parent folder, followed by files, by null characters.
            gen = split_null_list(pfile)
            parent = next(gen)
            return [parent + "\\" + f for f in gen] or [parent]
        else:
            return []
    else:
        if ok:
            return file.value
        else:
            return ''

def save_file(title, filetypes):
    file = ctypes.create_unicode_buffer(BUFFER_SIZE)
    pfile = ctypes.cast(file, ctypes.c_wchar_p)

    # Default options
    opts = tagOFNW(
        lStructSize=ctypes.sizeof(tagOFNW),

        lpstrFile=pfile,
        nMaxFile=BUFFER_SIZE,

        lpstrTitle=title,
        Flags=0x0008000A
    )

    # Filetypes
    if filetypes:
        out = []
        for s, t in filetypes:
            out.append(f'{s} ({t})\0{";".join(t.split())}\0')
        
        buf = ctypes.create_unicode_buffer(''.join(out)+'\0')
        
        opts.lpstrFilter = LPCWSTR(ctypes.addressof(buf))
        opts.lpstrDefExt = LPCWSTR(ctypes.addressof(buf))
    
    # Call file dialog
    ok = comdlg32.GetSaveFileNameW(ctypes.byref(opts))

    # Return data
    if ok:
        return file.value
    else:
        return ''

# Code simplified and turned into python bindings from the tk8.6.12/win/tkWinDialog.c file.
# tk is licensed here: https://www.tcl.tk/software/tcltk/license.html
def directory(title):
    # Create dialog
    ifd = ctypes.POINTER(IFileOpenDialog)()
    
    ole32.OleInitialize(None)
    try:
        hr = ole32.CoCreateInstance(
            ctypes.byref(ClsidFileOpenDialog),
            None,
            1,
            ctypes.byref(IIDIFileOpenDialog),
            ctypes.byref(ifd)
        )
        if hr < 0: raise OSError("Failed to create dialog")

        # Set options
        flags = UINT(0)
        hr = ifd.contents.lpVtbl.contents.GetOptions(ifd, ctypes.byref(flags))
        if hr < 0: raise OSError("Failed to get options")

        flags = UINT(flags.value | 0x1020)
        hr = ifd.contents.lpVtbl.contents.SetOptions(ifd, flags)

        # Set title
        if title is not None: ifd.contents.lpVtbl.contents.SetTitle(ifd, title)

        try:
            hr = ifd.contents.lpVtbl.contents.Show(ifd, None)
        except OSError:
            return ''
    
        # Acquire selection result
        resultIf = LPIShellItem()
        try:
            hr = ifd.contents.lpVtbl.contents.GetResult(ifd, ctypes.byref(resultIf))
            if hr < 0: raise OSError("Failed to get result of directory selection")
            wstr = LPWSTR()
            hr = resultIf.contents.lpVtbl.contents.GetDisplayName(resultIf, 0x80058000, ctypes.byref(wstr))
            if hr < 0: raise OSError("Failed to get display name from shell item")
            val = wstr.value
            ole32.CoTaskMemFree(wstr)
            return val
        finally:
            resultIf.contents.lpVtbl.contents.Release(resultIf)
    finally:
        ole32.OleUninitialize()


# For where the magic numbers come from, see https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw

def info(title, message):
    user32.MessageBoxW(None, message or "", title or "Message", 0x00000040)

def warning(title, message):
    user32.MessageBoxW(None, message or "", title or "Warning", 0x00000030)

def error(title, message):
    user32.MessageBoxW(None, message or "", title or "Error", 0x00000010)

def yesno(title, message):
    if user32.MessageBoxW(None, message or "", title or "", 0x00000024) == 6:
        return YES
    else:
        return NO

def yesnocancel(title, message):
    r = user32.MessageBoxW(None, message or "", title or "", 0x00000023)

    if r == 2:
        return CANCEL
    elif r == 6:
        return YES
    else:
        return NO

def retrycancel(title, message):
    if user32.MessageBoxW(None, message or "", title or "", 0x00000025) == 4:
        return RETRY
    else:
        return CANCEL

def okcancel(title, message):
    if user32.MessageBoxW(None, message or "", title or "", 0x00000021) == 1:
        return OK
    else:
        return CANCEL