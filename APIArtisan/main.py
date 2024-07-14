import json

from nicegui import ui, app

from .pages import page_builder
from .utils import screen_size, storage
from .constants import globals, storage_constants
from .models.display_mode import DisplayMode

storage.create_if_doesnt_exist()
settings = storage.load_settings_from_file()
try:
    dark_mode = settings["general"]["dark_mode"] == DisplayMode.DARK.value
except KeyError:
    dark_mode = True

print(f"Initiating {globals.APP_TITLE} with settings:")
print(json.dumps(settings, indent=storage_constants.INDENTATION))

page_builder.create_pages()

screen_size = screen_size.get_screen_size()

app.native.start_args["debug"] = globals.APP_DEBUG

ui.run(
    native=True,
    window_size=((screen_size.width, screen_size.height)),
    port=globals.APP_PORT,
    title=globals.APP_TITLE,
    dark=dark_mode,
    show_welcome_message=globals.APP_SHOW_WELCOME_MESSAGE,
    reload=False,
    favicon=globals.APP_FAVICON,
)
