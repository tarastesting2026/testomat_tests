from faker import Faker

from src.web.Application import Application

TARGET_PROJECT = "ZDc"

faker = Faker()


def test_login_with_valid_creds(app: Application, login):
    target_project_name = Faker().company()

    (app.new_projects_page
     .open().is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())


def test_new_page_elements(app: Application, login):
    app.new_projects_page.open()
    app.new_projects_page.is_loaded()


def test_new_project_creation(app: Application, login):
    app.new_projects_page.open()
    app.new_projects_page.is_loaded()

    target_project_name = Faker().company()
    app.new_projects_page.fill_project_title(target_project_name)
    app.new_projects_page.click_create()

    app.project_page.is_loaded()

    app.new_projects_page.open()
    app.new_projects_page.is_loaded()
