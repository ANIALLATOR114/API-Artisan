import json

from functools import partial
from nicegui import ui

from APIArtisan.models.secret import Secret
from APIArtisan.utils import storage

from ..models.config import Config
from ..models.auth_type import AuthType


def update_auth_from_secret_func(
    secret: Secret, config: Config, value_to_update: str, input_to_update: ui.input
):
    config.set_auth_details({value_to_update: secret.value})
    input_to_update.set_value(secret.value)
    ui.notify(f"Updated {value_to_update} with {secret.name}")


def build_secret_dropdown(
    secrets: list[Secret], config: Config, value_to_update: str, input_to_update: ui.input
):
    with ui.dropdown_button("Choose secret", auto_close=True):
        with ui.list():
            for secret in secrets:
                update_auth_from_secret = partial(
                    update_auth_from_secret_func, secret, config, value_to_update, input_to_update
                )
                with ui.item(on_click=partial(update_auth_from_secret)):
                    with ui.item_section():
                        ui.item_label(f"{secret.name} - {secret.description}")


@ui.refreshable
def build_auth_details(config: Config):
    secrets_dicts = storage.secrets.read_all_from_file()
    secrets = [Secret.from_dict(secret_dict) for secret_dict in secrets_dicts]
    enabled_secrets = [secret for secret in secrets if secret.available]

    match config.auth_type:
        case AuthType.BASIC:
            with ui.row():
                username_input = ui.input(
                    "Username",
                    value=config.auth_details.get("username", ""),
                    on_change=lambda value: config.set_auth_details({"username": value.value}),
                    password=True,
                )
                build_secret_dropdown(enabled_secrets, config, "username", username_input)

            with ui.row():
                password_input = ui.input(
                    "Password",
                    value=config.auth_details.get("password", ""),
                    on_change=lambda value: config.set_auth_details({"password": value.value}),
                    password=True,
                )
                build_secret_dropdown(enabled_secrets, config, "password", password_input)
        case AuthType.BEARER:
            with ui.row():
                token_input = ui.input(
                    "Token",
                    value=config.auth_details.get("token", ""),
                    on_change=lambda value: config.set_auth_details({"token": value.value}),
                    password=True,
                )
                build_secret_dropdown(enabled_secrets, config, "token", token_input)
        case AuthType.OAUTH:
            with ui.row():
                client_id_input = ui.input(
                    "Client ID",
                    value=config.auth_details.get("client_id", ""),
                    on_change=lambda value: config.set_auth_details({"client_id": value.value}),
                    password=True,
                )
                build_secret_dropdown(enabled_secrets, config, "client_id", client_id_input)
            with ui.row():
                client_secret_input = ui.input(
                    "Client Secret",
                    value=config.auth_details.get("client_secret", ""),
                    on_change=lambda value: config.set_auth_details({"client_secret": value.value}),
                    password=True,
                )
                build_secret_dropdown(enabled_secrets, config, "client_secret", client_secret_input)
        case AuthType.NONE:
            pass


def set_and_refresh_auth(config: Config, auth_type: AuthType):
    auth_enum = AuthType(auth_type)
    config.set_auth_type(auth_enum)
    build_auth_details.refresh(config)


async def update_config_and_refresh_list(config: Config):
    await config.update()
    build_auth_list.refresh(config)


@ui.refreshable
def build_auth_list(config: Config):
    if config.auth_enabled:
        ui.toggle(
            [auth.value for auth in AuthType],
            value=config.auth_type.value,
            on_change=lambda value: set_and_refresh_auth(config, value.value),
        )
        build_auth_details(config)


def generate_main_config_page(config: Config, main_body: ui.card):
    main_body.clear()
    with main_body:
        ui.markdown(f"### {config.name}")

        ui.separator()
        with ui.card():
            ui.markdown("##### Authentication")
            ui.switch(
                "Use authentication",
                on_change=lambda: (config.toggle_auth(), build_auth_list.refresh(config)),
                value=config.auth_enabled,
            )
            build_auth_list(config)

        ui.separator()
        with ui.card():
            ui.markdown("##### HTTP Configuration")
            with ui.row():
                with ui.card_section():
                    ui.label("HTTP Method")
                    ui.select(
                        ["GET", "POST", "PUT", "DELETE", "PATCH"],
                        value=config.http_config.method.value,
                        on_change=lambda value: config.http_config.set_method(value.value),
                    )
                with ui.card_section():
                    ui.label("Endpoint URL")
                    ui.input(
                        value=config.http_config.url,
                        on_change=lambda value: config.http_config.set_url(value.value),
                    )
                

            with ui.card_section():
                ui.label("Headers")
                ui.json_editor(
                    {
                        "content": {"json": config.http_config.headers},
                        "mode": "text",
                        "mainMenuBar": False,
                    },
                    on_change=lambda value: config.http_config.set_headers(
                        json.loads(value.content["text"])
                    ),
                )

            with ui.card_section():
                ui.label("Body")
                ui.json_editor(
                    {
                        "content": {"json": config.http_config.body},
                        "mode": "text",
                        "mainMenuBar": False,
                    },
                    on_change=lambda value: config.http_config.set_body(
                        json.loads(value.content["text"])
                    ),
                )

        ui.separator()
        with ui.card():
            ui.markdown("##### Control Flow Configuration")

            with ui.row():
                with ui.card_section():
                    ui.markdown("###### Retries")
                    ui.switch("Retry on failure")
                    ui.number(
                        "Retry count", value=1, min=1, max=10, step=1, precision=0, format="%.0f"
                    )

                with ui.card_section():
                    ui.markdown("###### Status codes")
                    ui.label(
                        "If undefined, all status codes that are not 2XX are considered errors"
                    )
                    ui.input("Successful (csv)")
                    ui.input("Unsuccessful (csv)")

        ui.separator()
        with ui.card():
            ui.markdown("##### Variable Substitution")
            ui.markdown(
                "Variables will be searched for in the body, headers, and URL in the format: `{{variable_name}}`\n\nExample URL with a variable  `https://api.example.com/users/{{user_id}}`"
            )

            with ui.row():
                with ui.card_section():
                    ui.markdown("###### Endpoint URL")
                    ui.switch("Variable substitution")
                    ui.input("Variable name")

                with ui.card_section():
                    ui.markdown("###### Body Payload")
                    ui.switch("Variable substitution")
                    ui.input("Variable name")

                with ui.card_section():
                    ui.markdown("###### Headers")
                    ui.switch("Variable substitution")
                    ui.input("Variable name")

        ui.separator()
        with ui.card():
            ui.markdown("##### Output Configuration")

            with ui.row():
                with ui.card_section():
                    with ui.column():
                        ui.markdown("###### Logs")
                        ui.switch("Console Logs", value=True)
                        ui.switch("Generic Disk Log", value=True)
                        ui.switch("Unique Disk Log", value=False)
                        ui.switch("Status Code", value=True)
                        ui.switch("Latency", value=False)
                        ui.switch("Response Body", value=False)

                with ui.card_section():
                    with ui.column():
                        ui.markdown("###### Response Body Format")
                        ui.label("Coming soon...")

        ui.button("Save", on_click=partial(update_config_and_refresh_list, config))
