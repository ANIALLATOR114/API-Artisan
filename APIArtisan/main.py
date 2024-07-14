import json

from nicegui import ui, app

from .pages import page_builder
from .utils import screen_size, storage
from .constants import globals, storage_constants

storage.create_if_doesnt_exist()
settings = storage.Settings()

print(f"Initiating {globals.APP_TITLE} with settings:")
print(json.dumps(settings.get_settings(), indent=storage_constants.INDENTATION))

page_builder.create_pages()

screen_size = screen_size.get_screen_size()

app.native.start_args["debug"] = settings.get_app_debug()
if settings.get_app_debug():
    print("Debug mode enabled.")
    print(f"Screen size: {screen_size.width}x{screen_size.height}")

ui.run(
    native=True,
    window_size=((screen_size.width, screen_size.height)),
    port=settings.get_app_port(),
    title=globals.APP_TITLE,
    dark=settings.get_dark_mode(),
    show_welcome_message=globals.APP_SHOW_WELCOME_MESSAGE,
    reload=False,
    favicon=globals.APP_FAVICON,
)
