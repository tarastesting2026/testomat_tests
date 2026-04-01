import re

import pytest
from faker import Faker
from playwright.sync_api import expect

from src.web.Application import Application

TARGET_PROJECT = "ZDc"
faker = Faker()

@pytest.mark.skip
def test_registered_email_is_correct(app: Application, configs, login):
    app.projects_page.is_loaded()

    app.page.locator("#user-menu-button").click()

    email_locator = app.page.locator(".auth-header-nav-right-dropdown-menu-block-email")

    expect(email_locator).to_be_visible()
    expect(email_locator).to_have_text(configs.email)

@pytest.mark.skip
def test_create_new_project(app: Application, login):
    app.projects_page.is_loaded()

    # Create project
    app.projects_page.header.click_create()

    project_name = faker.address()
    suite_name = faker.word()
    test_name = faker.word()

    app.page.get_by_placeholder("My Project").fill(project_name)
    app.page.locator('input[value="Create"]').click()

    app.page.get_by_text("I got it, let's start!").click()

    expect(app.page.locator(".sticky-header h2")).to_have_text(project_name)

    # Create suite
    app.page.get_by_placeholder("First Suite").fill(suite_name)
    app.page.get_by_role("button", name="Suite").click()

    expect(app.page.get_by_role("link", name=suite_name)).to_be_visible()

    # Create test
    app.page.get_by_role("link", name="New test").click()

    input_field = app.page.get_by_placeholder("Enter test name")
    input_field.fill(test_name)
    input_field.press("Enter")

    expect(app.page.get_by_text(test_name, exact=True)).to_be_visible()

    # Delete project
    app.page.on("dialog", lambda dialog: dialog.accept())

    app.page.locator("a:has(svg.md-icon-cog)").click()
    app.page.get_by_role("button", name="Administration").click()
    app.page.get_by_role("button", name="Delete Project").click()

    expect(
        app.page.get_by_text("Project will be deleted in few minutes")
    ).to_be_visible()

    # Back to projects page
    app.page.locator("button.btn-open").click()
    app.page.locator("a.logo-full").click()

    # Verify project is deleted
    app.projects_page.is_loaded()

    expect(
        app.page.get_by_role("heading", name=project_name)
    ).to_be_hidden()

@pytest.mark.skip
def test_card_title_matches_and_badges_present(app: Application, login):
    app.projects_page.is_loaded()

    card = app.projects_page.get_project_by_name("CucumberJS Demo Project")

    expect(card.title).to_have_text("CucumberJS Demo Project")
    expect(card.badges).not_to_have_count(0)

@pytest.mark.skip
def test_clear_search_restores_projects(app: Application, login):
    app.projects_page.is_loaded()

    app.projects_page.search_project("Gloves")
    app.projects_page.projects_count_is(1)

    app.projects_page.search_project("")

    expect(app.projects_page.project_cards).not_to_have_count(1)

@pytest.mark.skip
def test_search_partial_match(app: Application, login):
    app.projects_page.is_loaded()

    app.projects_page.search_project("Leather")

    app.projects_page.project_visible("Lightweight Leather Gloves")

@pytest.mark.skip
def test_search_no_results(app: Application, login):
    app.projects_page.is_loaded()

    app.projects_page.search_project("NON_EXISTING_PROJECT_123")

    app.projects_page.projects_count_is(0)

@pytest.mark.skip
def test_plan_badge_shows_enterprise(app: Application, login):
    app.projects_page.is_loaded()

    expect(app.projects_page.header.plan_badge).to_contain_text("Enterprise")

@pytest.mark.skip
def test_switch_back_to_grid_view(app: Application, login):
    app.projects_page.is_loaded()
    app.projects_page.header.switch_to_table_view()
    app.projects_page.header.switch_to_grid_view()

    expect(app.projects_page.header.grid_view_button).to_have_class("tablinks active_list_type")
    expect(app.projects_page.header.grid_view_button).to_have_attribute(
        "class", re.compile("active_list_type")
    )

@pytest.mark.skip
def test_get_demo_cards_returns_one(app: Application, login):
    app.projects_page.is_loaded()

    demo_cards_locator = app.projects_page.project_cards.filter(
        has=app.page.locator(".common-badge-project-demo")
    )

    expect(demo_cards_locator).to_have_count(1)


def test_non_demo_card_has_no_demo_badge(logged_app: Application):
    card = logged_app.projects_page.get_project_by_title("Gaines Group")
    expect(card.badges.filter(has_text="Demo")).to_have_count(0)

@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(logged_app: Application):
    logged_app.projects_page.navigate()

    logged_app.projects_page.verify_page_loaded()

    logged_app.projects_page.header.get_selected_company("QA Club Lviv")
    logged_app.projects_page.header.get_plan_name("Enterprise plan")

    target_project_name = "CucumberJS Demo Project"
    logged_app.projects_page.header.select_project(target_project_name)
    logged_app.projects_page.count_of_project_visibility(1)
    target_project = logged_app.projects_page.get_project_by_title(target_project_name)
    target_project.has_badge("Demo")