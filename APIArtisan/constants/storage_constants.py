import os

from ..models.display_mode import DisplayMode
from .globals import APP_DEFAULT_PORT, APP_DEFAULT_DEBUG

# Settings
GENERAL_KEY = "general"
DARK_MODE_KEY = "dark_mode"
DARK_MODE_DEFAULT = DisplayMode.DARK.value
APP_PORT_KEY = "app_port"
APP_DEBUG_KEY = "app_debug"
INDENTATION = 2

# Default settings
DEFAULT_SETTINGS = {
    GENERAL_KEY: {
        DARK_MODE_KEY: DisplayMode.DARK.value,
        APP_PORT_KEY: APP_DEFAULT_PORT,
        APP_DEBUG_KEY: APP_DEFAULT_DEBUG,
    }
}

# Paths
LOCAL_APP_DATA = os.path.expandvars(r"%LOCALAPPDATA%\APIArtisan")
SETTINGS_JSON = os.path.join(LOCAL_APP_DATA, "settings.json")
SECRETS_DIR = os.path.join(LOCAL_APP_DATA, "secrets")
CONFIGS_DIR = os.path.join(LOCAL_APP_DATA, "configs")
