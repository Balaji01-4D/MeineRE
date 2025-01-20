# Code simplified and turned into python bindings from the tk8.6.12/win/tkWinDialog.c file.
# tk is licensed here: https://www.tcl.tk/software/tcltk/license.html

import ctypes 
from ctypes.wintypes import *
from typing import Tuple

LPLPWSTR = ctypes.POINTER(LPWSTR)
LPVOIDP = ctypes.POINTER(ctypes.c_void_p)

LPOFNHOOKPROC = ctypes.WINFUNCTYPE(ctypes.POINTER(UINT), HWND, UINT, WPARAM, LPARAM)


class tagOFNW(ctypes.Structure):
    _fields_ = [
        ("lStructSize",         DWORD),
        ("hwndOwner",           HWND),
        ("hInstance",           HINSTANCE),
        ("lpstrFilter",         LPCWSTR),
        ("lpstrCustomFilter",   LPWSTR),
        ("nMaxCustFilter",      DWORD),
        ("nFilterIndex",        DWORD),
        ("lpstrFile",           LPWSTR),
        ("nMaxFile",            DWORD),
        ("lpstrFileTitle",      LPWSTR),
        ("nMaxFileTitle",       DWORD),
        ("lpstrInitialDir",     LPCWSTR),
        ("lpstrTitle",          LPCWSTR),
        ("Flags",               DWORD),
        ("nFileOffset",         WORD),
        ("nFileExtension",      WORD),
        ("lpstrDefExt",         LPCWSTR),
        ("lCustData",           LPARAM),
        ("lpfnHook",            LPOFNHOOKPROC),
        ("lpTemplateName",      LPCWSTR),
        ("pvReserved",          ctypes.c_void_p),
        ("dwReserved",          DWORD),
        ("FlagsEx",             DWORD)
    ]

    def __init__(self, *args, **kwargs):
        ctypes.memset(ctypes.pointer(self), 0, ctypes.sizeof(tagOFNW))
        super().__init__(*args, **kwargs)


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8)
    ]

    def __init__(self, data1: int, data2: int, data3: int, data4: Tuple[int], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Data1 = data1
        self.Data2 = data2
        self.Data3 = data3

        arr = self.Data4
        for i in range(8):
            arr[i] = data4[i]

CLSID = GUID
IID = GUID
REFGUID = ctypes.POINTER(GUID)
REFIID = ctypes.POINTER(GUID)

ClsidFileOpenDialog = CLSID(
    0xDC1C5A9C, 0xE88A, 0X4DDE, (0xA5, 0xA1, 0x60, 0xF8, 0x2A, 0x20, 0xAE, 0xF7)
)
IIDIFileOpenDialog = IID(
    0xD57C7288, 0xD4AD, 0x4768, (0xBE, 0x02, 0x9D, 0x96, 0x95, 0x32, 0xD9, 0x60)
)



SFGAOF = ULONG
SICHINTF = DWORD
LPSFGAOF = ctypes.POINTER(SFGAOF)
LPLPOLESTR = ctypes.POINTER(LPOLESTR)
FILEOPENDIALOGOPTIONS = DWORD
LPFILEOPENDIALOGOPTIONS = ctypes.POINTER(FILEOPENDIALOGOPTIONS)

# System dependent enums, could be wrong (I believe this is c_uint)
FDAP = ctypes.c_uint
SIGDN = ctypes.c_uint
SIATTRIBFLAGS = ctypes.c_uint

# Not useful for now
IBindCtx = ctypes.c_void_p
LPIBindCtx = LPVOIDP



# Single shell item class
class IShellItem(ctypes.Structure): pass

LPIShellItem = ctypes.POINTER(IShellItem)
LPLPIShellItem = ctypes.POINTER(ctypes.POINTER(IShellItem))

class IShellItemVtbl(ctypes.Structure):
    _fields_ = [
        ('QueryInterface',  ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItem, REFIID, LPVOIDP)),
        ('AddRef',          ctypes.WINFUNCTYPE(ULONG, LPIShellItem)),
        ('Release',         ctypes.WINFUNCTYPE(ULONG, LPIShellItem)),
        ('BindToHandler',   ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItem, LPIBindCtx, REFGUID, REFIID, LPVOIDP)),
        ('GetParent',       ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItem, LPLPIShellItem)),
        ('GetDisplayName',  ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItem, SIGDN, LPLPOLESTR)),
        ('GetAttributes',   ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItem, SFGAOF, LPSFGAOF)),
        ('Compare',         ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItem, LPIShellItem, SICHINTF, ctypes.POINTER(ctypes.c_int))),
    ]

IShellItem.\
    _fields_ = [("lpVtbl", ctypes.POINTER(IShellItemVtbl))]


# Multiple shell item class
class IShellItemArray(ctypes.Structure): pass

LPIShellItemArray = ctypes.POINTER(IShellItem)
LPLPIShellItemArray = ctypes.POINTER(ctypes.POINTER(IShellItem))

class IShellItemArrayVtbl(ctypes.Structure):
    _fields_ = [
        ('QueryInterface',              ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItemArray, REFIID, LPVOIDP)),
        ('AddRef',                      ctypes.WINFUNCTYPE(ULONG, LPIShellItemArray)),
        ('Release',                     ctypes.WINFUNCTYPE(ULONG, LPIShellItemArray)),
        ('BindToHandler',               ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItemArray, LPIBindCtx, REFGUID, REFIID, LPVOIDP)),
        ('GetPropertyStore',            ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItemArray, ctypes.c_int,  REFIID, LPVOIDP)),
        ('GetPropertyDescriptionList',  ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItemArray, ctypes.c_void_p, REFIID, LPVOIDP)),
        ('GetAttributes',               ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItemArray, SIATTRIBFLAGS, SFGAOF, LPSFGAOF)),
        ('GetCount',                    ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItemArray, LPDWORD)),
        ('GetItemAt',                   ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItemArray, DWORD, LPLPIShellItem)),
        ('EnumItems',                   ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIShellItemArray, LPVOIDP)),
    ]

IShellItemArray.\
    _fields_ = [("lpVtbl", ctypes.POINTER(IShellItemArrayVtbl))]


# file open dialog
class IFileOpenDialog(ctypes.Structure): pass

LPIFileOpenDialog = ctypes.POINTER(IFileOpenDialog)
LPTCLCOMDLG_FILTERSPEC = ctypes.c_void_p

class IFileOpenDialogVtbl(ctypes.Structure):
    _fields_ = [
        ('QueryInterface',          ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, REFIID, LPVOIDP)),
        ('AddRef',                  ctypes.WINFUNCTYPE(ULONG, LPIFileOpenDialog)),
        ('Release',                 ctypes.WINFUNCTYPE(ULONG, LPIFileOpenDialog)),
        ('Show',                    ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, HWND)),
        ('SetFileTypes',            ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, UINT, LPTCLCOMDLG_FILTERSPEC)),
        ('SetFileTypeIndex',        ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, UINT)),
        ('GetFileTypeIndex',        ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPUINT)),
        ('Advise',                  ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, ctypes.c_void_p, LPDWORD)),
        ('Unadvise',                ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, DWORD)),
        ('SetOptions',              ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, FILEOPENDIALOGOPTIONS)),
        ('GetOptions',              ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPFILEOPENDIALOGOPTIONS)),
        ('SetDefaultFolder',        ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPIShellItem)),
        ('SetFolder',               ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPIShellItem)),
        ('GetFolder',               ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPLPIShellItem)),
        ('GetCurrentSelection',     ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPLPIShellItem)),
        ('SetFileName',             ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPCWSTR)),
        ('GetFileName',             ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPLPWSTR)),
        ('SetTitle',                ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPCWSTR)),
        ('SetOkButtonLabel',        ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPCWSTR)),
        ('SetFileNameLabel',        ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPCWSTR)),
        ('GetResult',               ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPLPIShellItem)),
        ('AddPlace',                ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPIShellItem, FDAP)),
        ('SetDefaultExtension',     ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPCWSTR)),
        ('Close',                   ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, ctypes.HRESULT)),
        ('SetClientGuid',           ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, REFGUID)),
        ('ClearClientData',         ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog)),
        ('SetFilter',               ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, ctypes.c_void_p)),
        ('GetResults',              ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPLPIShellItemArray)),
        ('GetSelectedItems',        ctypes.WINFUNCTYPE(ctypes.HRESULT, LPIFileOpenDialog, LPLPIShellItemArray)),
    ]

IFileOpenDialog.\
    _fields_ = [("lpVtbl", ctypes.POINTER(IFileOpenDialogVtbl))]