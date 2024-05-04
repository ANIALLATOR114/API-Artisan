from enum import Enum
import json
from nicegui import ui
from ..utils import storage

from .auth_type import AuthType
from .http_config import HTTPConfig
from ..utils.storage import INDENTATION


class Config:
    def __init__(
        self,
        name: str,
        auth_enabled: bool = False,
        auth_type: AuthType = AuthType.NONE,
        auth_details: dict = {},
        http_config: HTTPConfig = HTTPConfig(),
    ) -> None:
        self.name = name
        self.auth_enabled = auth_enabled
        self.auth_type = auth_type
        self.auth_details = auth_details
        self.http_config = http_config

    def to_json(self):
        return json.dumps(
            self, indent=INDENTATION, default=lambda o: str(o) if isinstance(o, Enum) else o.__dict__
        )
    
    async def save(self):
        try:
            json = self.to_json()
            await storage.configs.write_to_file(json, self.name)
        except FileExistsError:
            ui.notify(f"A config with this name {self.name} already exists!", type="negative")
            return
        ui.notify(
            f"Config {self.name} successfully saved!",
            type="positive",
        )

    async def update(self):
        try:
            json = self.to_json()
            await storage.configs.update_file(json, self.name)
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
        data["http_config"] = HTTPConfig.from_dict(data.get("http_config", {}))
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
