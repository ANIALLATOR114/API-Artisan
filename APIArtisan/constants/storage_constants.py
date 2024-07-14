import os

from ..models.display_mode import DisplayMode

DEFAULT_SETTINGS = {"general": {"dark_mode": DisplayMode.DARK.value}}
LOCAL_APP_DATA = os.path.expandvars(r"%LOCALAPPDATA%\APIArtisan")
SETTINGS_JSON = os.path.join(LOCAL_APP_DATA, "settings.json")
SECRETS_DIR = os.path.join(LOCAL_APP_DATA, "secrets")
CONFIGS_DIR = os.path.join(LOCAL_APP_DATA, "configs")
INDENTATION = 2
