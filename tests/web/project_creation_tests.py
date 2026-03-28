from faker import Faker

from src.web.Application import Application

TARGET_PROJECT = "ZDc"
faker = Faker()


def test_login_with_valid_creds(login, app: Application):
    target_project_name = Faker().company()

    (app.new_projects_page
     .open().is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

    (app.project_page.side_bar
     .is_loaded()
     .click_logo()
     .expect_tab_active("Tests"))
