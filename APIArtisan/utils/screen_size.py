import ctypes

from typing import NamedTuple


class ScreenSize(NamedTuple):
    width: int
    height: int


def get_screen_size() -> ScreenSize:
    """
    Get the screen size by using the GetSystemMetrics function from the user32 library.

    Returns:
        ScreenSize: An instance of the ScreenSize class representing the width and height of the screen.
    """
    user32 = ctypes.windll.user32
    screen_width = int(user32.GetSystemMetrics(0) * 0.6)
    screen_height = int(user32.GetSystemMetrics(1) * 0.6)
    return ScreenSize(width=screen_width, height=screen_height)
