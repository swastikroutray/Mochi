import ctypes
import sys
from ctypes import wintypes


def active_window_title() -> str:
    """Return the foreground window title on Windows; empty elsewhere for now."""
    if sys.platform != "win32":
        return ""

    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return ""

    length = user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value.strip()
