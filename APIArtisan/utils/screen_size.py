import os
import ctypes
import subprocess

from typing import NamedTuple

from ..constants import globals


class ScreenSize(NamedTuple):
    width: int
    height: int


def get_screen_size() -> ScreenSize:
    """
    Get the screen size.

    On Windows, this uses the GetSystemMetrics function from the user32 library.
    On non-Windows systems, this uses the 'xrandr' command.

    Returns:
        ScreenSize: An instance of the ScreenSize class representing the width and height of the screen.
    """
    try:
        if os.name == "nt":  # Windows
            user32 = ctypes.windll.user32
            screen_width = int(user32.GetSystemMetrics(0) * 0.7)
            screen_height = int(user32.GetSystemMetrics(1) * 0.7)
        elif os.name == "posix":
            xrandr = subprocess.Popen(["xrandr"], stdout=subprocess.PIPE)
            output = subprocess.check_output(["grep", "*"], stdin=xrandr.stdout)
            output = output.decode("utf-8")
            screen_width = int(output.split()[0] * 0.7)
            screen_height = int(output.split()[1] * 0.7)
        else:
            screen_width = globals.DEFAULT_SCREEN_WIDTH
            screen_height = globals.DEFAULT_SCREEN_HEIGHT
    except Exception:
        screen_width = globals.DEFAULT_SCREEN_WIDTH
        screen_height = globals.DEFAULT_SCREEN_HEIGHT

    return ScreenSize(width=screen_width, height=screen_height)