import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from util.conf import CONFLUENCE_SETTINGS

from selenium_ui.confluence.pages.pages import Login, AllUpdates, PopupManager, Page, Dashboard, TopNavPanel, Editor, \
    Logout


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_pages']:
        app_specific_page_id = datasets['custom_page_id']

    @print_timing("selenium_app_custom_action")
    def measure():

        @print_timing("selenium_app_custom_action:view_page")
        def sub_measure():
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/pages/viewpage.action?pageId={app_specific_page_id}")
            page.wait_until_visible((By.ID, "title-text"))  # Wait for title field visible
            page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()

def app_specific_action_create_confluence_page(webdriver, datasets):
    nav_panel = TopNavPanel(webdriver)
    create_page = Editor(webdriver)

    @print_timing("selenium_app_specific_action_create_page")
    def measure():

        @print_timing("selenium_app_specific_action_create_page:open_create_page_editor")
        def sub_measure():
            nav_panel.click_create()
            PopupManager(webdriver).dismiss_default_popup()
            create_page.wait_for_create_page_open()
        sub_measure()

        PopupManager(webdriver).dismiss_default_popup()

        create_page.write_title()
        create_page.write_content()

        @print_timing("selenium_app_specific_action_create_page:save_created_page")
        def sub_measure():
            create_page.click_submit()
            page = Page(webdriver)
            page.wait_for_page_loaded()
        sub_measure()
    measure()