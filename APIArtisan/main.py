import json

from nicegui import ui, app

from .pages import page_builder
from .utils import screen_size, storage

storage.create_if_doesnt_exist()
settings = storage.load_settings_from_file()
try:
    dark_mode = settings["general"]["dark_mode"] == storage.DisplayMode.DARK.value
except KeyError:
    dark_mode = True

print("Initiating API Artisan with settings:")
print(json.dumps(settings, indent=2))

page_builder.create_pages()

screen_size = screen_size.get_screen_size()

app.native.start_args["debug"] = True

ui.run(
    native=True,
    window_size=((screen_size.width, screen_size.height)),
    port=9999,
    title="API Artisan",
    dark=dark_mode,
    show_welcome_message=False,
    reload=False,
    favicon="🚀",
)
