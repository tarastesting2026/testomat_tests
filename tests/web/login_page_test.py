import pytest

from src.web import Application
from tests.data.login_test_data import invalid_login_test_data


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("email, password", invalid_login_test_data)
def test_login_invalid(shared_app: Application, email: str, password: str):
    shared_app.login_page.open()
    shared_app.login_page.is_loaded()
    shared_app.login_page.login_user(email, password)
    shared_app.login_page.invalid_login_message_visible()
    shared_app.page.wait_for_timeout(2000)


@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(logged_app: Application):
    logged_app.projects_page.is_loaded()
