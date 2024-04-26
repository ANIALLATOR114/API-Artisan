from functools import partial
from nicegui import ui

from .base_page import BasePage
from ..utils import storage
from ..models.config import Config
from .main_config import generate_main_config_page


async def delete_config_func(config: Config, main_body: ui.card):
    with ui.dialog() as confirm, ui.card():
        ui.label(f"Are you sure you want to delete {config.name}?")
        with ui.row():
            ui.button("Yes delete", on_click=lambda: confirm.submit("Yes"))
            ui.space()
            ui.button("Cancel", color="red", on_click=lambda: confirm.submit("No"))

    result = await confirm
    if result == "Yes":
        await config.delete()
        confirm.clear()
        main_body.clear()
        build_configs_list.refresh()
    else:
        confirm.clear()


@ui.refreshable
def build_configs_list(main_body: ui.card):
    configs_dicts = storage.configs.read_all_from_file()
    configs = [Config.from_dict(config_dict) for config_dict in configs_dicts]

    with ui.list().classes("w-full"):
        if len(configs) == 0:
            ui.markdown("You don't have any configurations yet, create one using the button above!")
        for config in configs:
            delete_config = partial(delete_config_func, config, main_body)
            view_config = partial(generate_main_config_page, config, main_body)

            ui.separator()
            with ui.item():
                with ui.item_section():
                    ui.markdown(f"##### {config.name}")
                    with ui.row():
                        ui.button(
                            "View",
                            on_click=view_config,
                        )
                        ui.button(
                            "Delete",
                            color="red",
                            on_click=delete_config,
                        )


def build_configuration_dialog():
    with ui.dialog(value=True) as dialog, ui.card():
        name = ui.input(
            label="Name",
            placeholder="Name the configuration",
            validation={
                "This name is too long": lambda value: len(value) < 30,
                "This name is too short": lambda value: len(value) > 3,
            },
        )

        async def save_config():
            if name.validate():
                config = Config(
                    name=name.value,
                )
                await config.save()
                build_configs_list.refresh()
                dialog.close()
            else:
                ui.notify("Validation error", type="negative")

        with ui.row():
            ui.button("Save", on_click=save_config)
            ui.space()
            ui.button("Cancel", color="red", on_click=dialog.close)


class SideMenu(BasePage):
    def __init__(self, main_body: ui.card) -> None:
        self.main_body = main_body

    def HEADER(self) -> str:
        return "Your Stored Configurations"

    def build_content(self):
        ui.markdown(f"##### {self.HEADER()}")

        ui.button("Create a configuration", on_click=build_configuration_dialog)

        build_configs_list(self.main_body)
