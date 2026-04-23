import pytest
from faker import Faker

from src.web import Application
from tests.fixtures.cookie_helper import CookieHelper

fake = Faker()


@pytest.mark.web
def test_add_feature_flag_cookie(logged_app: Application, cookies: CookieHelper):
    cookies.add("feature_flag", "dark_mode_enabled", "app.testomat.io")

    assert cookies.exists("feature_flag")
    assert cookies.get_value("feature_flag") == "dark_mode_enabled"

    logged_app.page.reload()


@pytest.mark.web
def test_clear_feature_flag_cookie(logged_app: Application, cookies: CookieHelper):
    cookies.add("feature_flag", "beta_feature", "app.testomat.io")

    assert cookies.exists("feature_flag")

    cookies.clear(name="feature_flag")
    assert not cookies.exists("feature_flag")
