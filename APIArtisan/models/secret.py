import json
from enum import Enum

from nicegui import ui
from ..utils import storage


class Secret:
    def __init__(self, name: str, value: str, description: str, available: bool):
        self.name = name
        self.description = description
        self.value = value
        self.available = available

    def to_json(self):
        return json.dumps(
            self,
            indent=storage.INDENTATION,
            default=lambda o: str(o) if isinstance(o, Enum) else o.__dict__,
        )

    async def set_availability(self, switch: ui.switch):
        self.available = switch.value

        json = self.to_json()
        try:
            await storage.secrets.update_file(json, self.name)
        except FileNotFoundError:
            ui.notify(f"Secret {self.name} does not exist!", type="negative")
            return
        ui.notify(
            f"Secret {self.name} availability set to {self.available}",
            type="info",
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Secret":
        return cls(**data)

    async def save(self):
        json = self.to_json()
        try:
            await storage.secrets.write_to_file(json, self.name)
        except FileExistsError:
            ui.notify(f"A secret with this name {self.name} already exists!", type="negative")
            return
        ui.notify(
            f"Secret {self.name} successfully saved!",
            type="positive",
        )

    async def delete(self):
        try:
            await storage.secrets.delete_file(self.name)
        except FileNotFoundError:
            ui.notify(f"Secret {self.name} does not exist!", type="negative")
            return
        ui.notify(
            f"Secret {self.name} successfully deleted!",
            type="positive",
        )
