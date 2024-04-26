from abc import ABC, abstractmethod

from nicegui import ui


class BasePage(ABC):
    @abstractmethod
    def HEADER(self) -> str:
        pass

    def build_header(self):
        ui.tab(self.HEADER())

    @abstractmethod
    def build_content(self):
        pass
