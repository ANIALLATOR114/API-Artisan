from nicegui import ui

from .base_page import BasePage


class AboutPage(BasePage):
    def HEADER(self) -> str:
        return "About"

    def build_content(self):
        with ui.tab_panel(self.HEADER()):
            ui.label("Content of About")
