from nicegui import ui
from ..utils import storage

from .auth_type import AuthType


class Config:
    def __init__(
        self,
        name: str,
        auth_enabled: bool = False,
        auth_type: AuthType = AuthType.NONE,
        auth_details: dict = {},
    ) -> None:
        self.name = name
        self.auth_enabled = auth_enabled
        self.auth_type = auth_type
        self.auth_details = auth_details

    async def save(self):
        try:
            await storage.configs.write_to_file(self)
        except FileExistsError:
            ui.notify(f"A config with this name {self.name} already exists!", type="negative")
            return
        ui.notify(
            f"Config {self.name} successfully saved!",
            type="positive",
        )

    async def update(self):
        try:
            await storage.configs.update_file(self)
        except FileNotFoundError:
            ui.notify(f"Config {self.name} does not exist!", type="negative")
            return
        ui.notify(
            f"Config {self.name} successfully updated!",
            type="positive",
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        data = data.copy()
        data["auth_type"] = AuthType(data.get("auth_type", AuthType.NONE))
        return cls(**data)

    async def delete(self):
        try:
            await storage.configs.delete_file(self.name)
        except FileNotFoundError:
            ui.notify(f"Config {self.name} does not exist!", type="negative")
            return
        ui.notify(
            f"Config {self.name} successfully deleted!",
            type="positive",
        )

    def toggle_auth(self):
        self.auth_enabled = not self.auth_enabled

    def set_auth_type(self, auth_type: AuthType):
        self.auth_type = auth_type

    def set_auth_details(self, auth_detail: dict):
        self.auth_details.update(auth_detail)
