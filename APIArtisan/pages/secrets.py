from functools import partial

from nicegui import ui

from ..utils import storage
from ..models.secret import Secret
from .base_page import BasePage


@ui.refreshable
def build_secrets_list():
    secrets_dicts = storage.secrets.read_all_from_file()
    secrets = [Secret(**secret_dict) for secret_dict in secrets_dicts]

    if len(secrets) == 0:
        ui.markdown("You don't have any secrets yet, create one using the button above!")

    with ui.list():
        for secret in secrets:

            async def delete_secret_func(secret: Secret):
                with ui.dialog() as confirm, ui.card():
                    ui.label(f"Are you sure you want to delete {secret.name}?")
                    with ui.row():
                        ui.button("Yes delete", on_click=lambda: confirm.submit("Yes"))
                        ui.space()
                        ui.button("Cancel", color="red", on_click=lambda: confirm.submit("No"))

                result = await confirm
                if result == "Yes":
                    await secret.delete()
                    confirm.clear()
                    build_secrets_list.refresh()
                else:
                    confirm.clear()

            def peek_secret_func(secret: Secret):
                ui.notify(secret.value, type="info")

            peek_secret = partial(peek_secret_func, secret)
            delete_secret = partial(delete_secret_func, secret)

            with ui.item():
                with ui.card():
                    ui.markdown(f"##### {secret.name}")
                    ui.markdown(secret.description)
                    with ui.row():
                        ui.switch(
                            "Available",
                            value=secret.available,
                            on_change=secret.set_availability,
                        )
                        ui.button(
                            "Peek 👀",
                            color="blue",
                            on_click=peek_secret,
                        )
                        ui.button(
                            "Delete",
                            color="red",
                            on_click=delete_secret,
                        )


def build_secret_dialog():
    with ui.dialog(value=True) as dialog, ui.card():
        name = ui.input(
            label="Name",
            placeholder="Name of the secret",
            validation={
                "This name is too long": lambda value: len(value) < 30,
                " This name is too short": lambda value: len(value) > 3,
            },
        )

        description = ui.input(
            label="Description",
            placeholder="Short description of the secret",
            validation={
                "This description is too long": lambda value: len(value) < 120,
            },
        )

        value = ui.input(
            label="The secret",
            placeholder="The value of the secret",
            validation={"This secret is too long": lambda value: len(value) < 8192},
            password=True,
            password_toggle_button=True,
        )

        available = ui.switch("Available for selection", value=True)

        async def save_secret():
            if name.validate() and value.validate() and description.validate():
                secret = Secret(
                    name=name.value,
                    value=value.value,
                    description=description.value,
                    available=available.value,
                )
                await secret.save()
                build_secrets_list.refresh()
                dialog.close()
            else:
                ui.notify("Validation error", type="negative")

        with ui.row():
            ui.button("Save", on_click=save_secret)
            ui.space()
            ui.button("Cancel", color="red", on_click=dialog.close)


class SecretsPage(BasePage):
    def HEADER(self) -> str:
        return "Secrets"

    def build_content(self):
        with ui.tab_panel(self.HEADER()).classes("p-0"):
            ui.markdown("#### Your Secrets")

            ui.button("Create a new secret", on_click=build_secret_dialog)
            ui.separator()
            build_secrets_list()
