import re

import pytest

from src.web.pages.LoginPage import LoginPage
from src.web.pages.ProjectsPage import ProjectsPage
from tests.conftest import Config

TARGET_PROJECT = "ZDc"
from playwright.sync_api import Page, expect
from faker import Faker

faker = Faker()


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)


def test_registered_email_is_correct(page: Page, configs, login):
    projects = ProjectsPage(page)

    projects.is_loaded()

    page.locator("#user-menu-button").click()

    email_locator = page.locator(".auth-header-nav-right-dropdown-menu-block-email")

    expect(email_locator).to_be_visible()
    expect(email_locator).to_have_text(configs.email)


def test_create_new_project(page: Page, login):
    projects_page = ProjectsPage(page)

    projects_page.is_loaded()

    # Create project
    projects_page.header.click_create()

    project_name = faker.address()
    suite_name = faker.word()
    test_name = faker.word()

    page.get_by_placeholder("My Project").fill(project_name)
    page.locator('input[value="Create"]').click()

    page.get_by_text("I got it, let's start!").click()

    expect(page.locator(".sticky-header h2")).to_have_text(project_name)

    # Create suite
    page.get_by_placeholder("First Suite").fill(suite_name)
    page.get_by_role("button", name="Suite").click()

    expect(page.get_by_role("link", name=suite_name)).to_be_visible()

    # Create test
    page.get_by_role("link", name="New test").click()

    input_field = page.get_by_placeholder("Enter test name")
    input_field.fill(test_name)
    input_field.press("Enter")

    expect(page.get_by_text(test_name, exact=True)).to_be_visible()

    # Delete project
    page.on("dialog", lambda dialog: dialog.accept())

    page.locator("a:has(svg.md-icon-cog)").click()
    page.get_by_role("button", name="Administration").click()
    page.get_by_role("button", name="Delete Project").click()

    expect(
        page.get_by_text("Project will be deleted in few minutes")
    ).to_be_visible()

    # Back to projects page
    page.locator("button.btn-open").click()
    page.locator("a.logo-full").click()

    # Verify project is deleted
    projects_page.is_loaded()

    expect(
        page.get_by_role("heading", name=project_name)
    ).to_be_hidden()


def test_card_title_matches_and_badges_present(page: Page, login):
    projects_page = ProjectsPage(page)

    projects_page.is_loaded()

    card = projects_page.get_project_by_name("CucumberJS Demo Project")

    expect(card.title).to_have_text("CucumberJS Demo Project")
    expect(card.badges).not_to_have_count(0)


def test_clear_search_restores_projects(page: Page, login):
    projects = ProjectsPage(page)

    projects.is_loaded()

    projects.search_project("Gloves")
    projects.projects_count_is(1)

    projects.search_project("")

    expect(projects.project_cards).not_to_have_count(1)


def test_search_partial_match(page: Page, login):
    projects = ProjectsPage(page)

    projects.is_loaded()

    projects.search_project("Leather")

    projects.project_visible("Lightweight Leather Gloves")


def test_search_no_results(page: Page, login):
    projects = ProjectsPage(page)

    projects.is_loaded()

    projects.search_project("NON_EXISTING_PROJECT_123")

    projects.projects_count_is(0)


def test_plan_badge_shows_enterprise(page: Page, login):
    projects = ProjectsPage(page)

    projects.is_loaded()

    expect(projects.header.plan_badge).to_contain_text("Enterprise")


def test_switch_back_to_grid_view(page: Page, login):
    projects = ProjectsPage(page)

    projects.is_loaded()

    projects.header.switch_to_table_view()
    projects.header.switch_to_grid_view()

    expect(projects.header.grid_view_button).to_have_class("tablinks active_list_type")
    expect(projects.header.grid_view_button).to_have_attribute(
        "class", re.compile("active_list_type")
    )


def test_get_demo_cards_returns_one(page: Page, login):
    projects_page = ProjectsPage(page)

    projects_page.is_loaded()

    demo_cards_locator = projects_page.grid.cards.filter(
        has=page.locator(".common-badge-project-demo")
    )

    expect(demo_cards_locator).to_have_count(1)


def test_non_demo_card_has_no_demo_badge(page: Page, login):
    projects_page = ProjectsPage(page)
    card = projects_page.grid.get_card_by_title("Gaines Group")
    expect(card.badges.filter(has_text="Demo")).to_have_count(0)
