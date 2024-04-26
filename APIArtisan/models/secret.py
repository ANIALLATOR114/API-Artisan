from nicegui import ui
from ..utils import storage


class Secret:
    def __init__(self, name: str, value: str, description: str, available: bool):
        self.name = name
        self.description = description
        self.value = value
        self.available = available

    async def set_availability(self, switch: ui.switch):
        self.available = switch.value
        try:
            await storage.secrets.update_file(self)
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
        try:
            await storage.secrets.write_to_file(self)
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
