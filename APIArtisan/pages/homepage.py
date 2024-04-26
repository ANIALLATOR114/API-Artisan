from nicegui import ui

from .base_page import BasePage


class HomePage(BasePage):
    def HEADER(self) -> str:
        return "Home"

    def build_content(self):
        with ui.tab_panel(self.HEADER()):
            ui.label("Content of homepage")
