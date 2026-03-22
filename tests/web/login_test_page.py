from operator import length_hint

import faker
from playwright.sync_api import Page

from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from tests.conftest import Config


def test_login_invalid(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(configs.email, faker.Faker().password(length=10))
    login_page.invalid_login_message_visible()