import os
from dataclasses import dataclass

import pytest
from load_dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.web import Application

load_dotenv()


def clear_browser_state(page: Page) -> None:
    page.context.clear_cookies()
    page.evaluate("window.localStorage.clear()")
    page.evaluate("window.sessionStorage.clear()")


def build_browser_context(browser: Browser, config) -> BrowserContext:
    return browser.new_context(
        base_url=config.app_base_url,
        viewport={"width": 1920, "height": 1080},
        locale="uk-UA",
        timezone_id="Europe/Kyiv",
        record_video_dir="videos/",
        permissions=["geolocation"],
    )


@dataclass(frozen=True)
class Config:
    base_url: str
    app_base_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_APP_URL"),
        app_base_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150, timeout=30000)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs: Config) -> Application:
    context = build_browser_context(browser_instance, configs)
    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


@pytest.fixture(scope="session")
def logged_context(browser_instance: Browser, configs: Config) -> BrowserContext:
    context = build_browser_context(browser_instance, configs)
    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    app.projects_page.is_loaded()
    page.close()
    yield context
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext) -> Application:
    page = logged_context.new_page()
    yield Application(page)
    page.close()


@pytest.fixture(scope="module")
def module_page(browser_instance: Browser, configs: Config) -> Page:
    context = build_browser_context(browser_instance, configs)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_app(module_page: Page) -> Application:
    yield Application(module_page)
    clear_browser_state(module_page)
