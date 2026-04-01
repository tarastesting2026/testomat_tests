import pytest
from faker import Faker

from src.web.Application import Application

TARGET_PROJECT = "ZDc"

faker = Faker()

@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(logged_app: Application):
    target_project_name = Faker().company()

    (logged_app.new_projects_page
     .open().is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (logged_app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

@pytest.mark.smoke
@pytest.mark.web
def test_new_page_elements(logged_app: Application):
    logged_app.new_projects_page.open()
    logged_app.new_projects_page.is_loaded()

@pytest.mark.smoke
@pytest.mark.web
def test_new_project_creation(logged_app: Application):
    logged_app.new_projects_page.open()
    logged_app.new_projects_page.is_loaded()

    target_project_name = Faker().company()
    logged_app.new_projects_page.fill_project_title(target_project_name)
    logged_app.new_projects_page.click_create()

    logged_app.project_page.is_loaded()

    logged_app.new_projects_page.open()
    logged_app.new_projects_page.is_loaded()
