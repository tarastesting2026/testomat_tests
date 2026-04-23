import os

import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.fixtures.config import Config

TARGET_PROJECT = "ZDc"


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    page.goto(configs.login_url)
    login_user(page, configs.email, configs.password)


@pytest.mark.skip("because we have removed playwright-pytest library")
def test_login_with_invalid_creds(page: Page, configs: Config):
    open_home_page(page)

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()
    invalid_password = Faker().password(length=10)

    login_user(page, configs.email, invalid_password)

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")


@pytest.mark.skip("because we have removed playwright-pytest library")
def test_search_project_in_company(page: Page, login):
    search_for_project(page, TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


@pytest.mark.skip("because we have removed playwright-pytest library")
def test_should_be_possible_to_open_free_project(page: Page, login):
    # actr
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    # assert
    target_project = "ZDc"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()

    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


@pytest.mark.skip("because we have removed playwright-pytest library")
def test_registered_email_is_correct(page: Page, configs: Config, login):
    page.locator("#user-menu-button").click()
    expect(page.locator(".auth-header-nav-right-dropdown-menu-block-email")).to_have_text(configs.email)


@pytest.mark.skip("because we have removed playwright-pytest library")
def test_create_new_project(page: Page, login):
    page.get_by_role("link", name="Create").click()

    project_name = Faker().address()
    suite_name = Faker().word()
    test_name = Faker().word()
    sidebar_settings_button = "a:has(svg.md-icon-cog)"

    page.locator("#user-menu-button").click()
    expect(page.locator(".auth-header-nav-right-dropdown-menu-block-email")) \
        .to_have_text("taras.testing.2026@gmail.com")

    page.get_by_placeholder("My Project").fill(project_name)
    page.locator('input[value="Create"]').click()
    page.get_by_text("I got it, let's start!").click()

    expect(page.locator(".sticky-header h2")).to_have_text(project_name)

    page.get_by_placeholder("First Suite").fill(suite_name)
    page.get_by_role("button", name="Suite").click()

    expect(page.locator("a", has_text=suite_name)).to_be_visible()

    page.get_by_role("link", name="New test").click()

    input_field = page.get_by_placeholder("Enter test name")
    input_field.fill(test_name)
    input_field.press("Enter")

    expect(page.get_by_text(test_name, exact=True)).to_be_visible()

    page.locator(sidebar_settings_button).click()

    # Click the "Administration" button and confirm the popup
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Administration").click()

    # Click the "Delete Project" button and confirm the popup
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete Project").click()

    expect(page.get_by_text("Project will be deleted in few minutes")).to_be_visible()

    page.locator("button.btn-open").click()
    page.locator("a.logo-full").click()

    expect(page.get_by_text(project_name)).not_to_be_visible()


def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def open_home_page(page: Page):
    page.goto(os.getenv("BASE_URL"))


def login_user(page: Page, email, password):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()
