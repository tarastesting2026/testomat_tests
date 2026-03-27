from src.web.pages.NewProjectsPage import NewProjectsPage
from src.web.pages.ProjectPage import ProjectPage

TARGET_PROJECT = "ZDc"
from playwright.sync_api import Page
from faker import Faker

faker = Faker()


def test_login_with_valid_creds(page: Page, login):
    target_project_name = Faker().company()

    (NewProjectsPage(page)
     .open().is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (ProjectPage(page)
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me(target_project_name))


def test_new_page_elements(page: Page, login):
    new_projecs = NewProjectsPage(page)
    new_projecs.open()
    new_projecs.is_loaded()


def test_new_project_creation(page: Page, login):
    new_projecs = NewProjectsPage(page)
    new_projecs.open()
    new_projecs.is_loaded()

    target_project_name = Faker().company()
    new_projecs.fill_project_title(target_project_name)
    new_projecs.click_create()

    ProjectPage(page).is_loaded()
