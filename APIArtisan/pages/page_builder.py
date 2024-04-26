from typing import Dict
from datetime import datetime
from nicegui import ui

from .base_page import BasePage
from .about import AboutPage
from .homepage import HomePage
from .secrets import SecretsPage
from .side_menu import SideMenu


def create_pages() -> None:
    """
    Creates and configures the pages for the application.

    Returns:
        None
    """
    pages: Dict[str, BasePage] = {
        "Home": HomePage(),
        "About": AboutPage(),
        "Secrets": SecretsPage(),
    }

    with ui.header().classes(replace="row items-center"):
        ui.space()
        timer = ui.label()
        ui.timer(1.0, lambda: timer.set_text(f"{datetime.now():%X} UTC"))

        with ui.tabs() as tabs:
            for page in pages.values():
                page.build_header()
        ui.button(
            on_click=lambda: right_drawer.toggle(),
            icon="menu",
        ).props("flat color=white")

    with ui.footer(value=False) as footer:
        ui.label("Footer")

    # tailwinds classes for take up max width as a container
    with ui.card().classes("w-full") as main_body:
        ui.label("Select a configuration")

    with ui.left_drawer(bordered=True):
        SideMenu(main_body).build_content()

    with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle, icon="contact_support").props("fab")

    with ui.right_drawer(bordered=True) as right_drawer:
        with ui.tab_panels(tabs, value=pages["Home"].HEADER()).classes("w-full"):
            for page in pages.values():
                page.build_content()
