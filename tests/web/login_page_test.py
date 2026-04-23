import pytest
from faker import Faker

from src.web import Application

fake = Faker()

invalid_login_test_data = [
    # -----------------------
    # ECP: Invalid email
    # -----------------------
    pytest.param("plainaddress", fake.password(10), id="email_no_at_symbol"),
    pytest.param("missingdomain@", fake.password(10), id="email_missing_domain"),
    pytest.param("@nouser.com", fake.password(10), id="email_missing_username"),
    pytest.param("user@.com", fake.password(10), id="email_invalid_domain"),
    pytest.param("user.com", fake.password(10), id="email_no_at_and_domain"),

    # -----------------------
    # ECP: Invalid password
    # -----------------------
    pytest.param(fake.email(), "", id="empty_password"),
    pytest.param(fake.email(), "      ", id="spaces_only_password"),

    # -----------------------
    # BVA: Password length boundaries
    # -----------------------
    pytest.param(fake.email(), "a" * 7, id="password_length_7_below_min"),
    pytest.param(fake.email(), "a" * 8, id="password_length_8_min_edge"),
    pytest.param(fake.email(), "a" * 65, id="password_length_65_above_max"),

    # -----------------------
    # ECP: Both invalid
    # -----------------------
    pytest.param("", "", id="empty_email_and_password"),
    pytest.param("invalid_email", "123", id="both_invalid_format"),

    # -----------------------
    # ECP: Invalid username instead of email
    # -----------------------
    pytest.param(fake.user_name(), fake.password(12), id="username_instead_of_email"),

    # -----------------------
    # BVA: Email boundaries
    # -----------------------
    pytest.param("a@b.c", fake.password(10), id="very_short_email_edge"),
    pytest.param("a" * 250 + "@test.com", fake.password(10), id="very_long_email_local_part"),

    # -----------------------
    # Special characters / injection-like inputs
    # -----------------------
    pytest.param("test@test.com", "' OR '1'='1", id="sql_injection_like_password"),
    pytest.param("<script>alert(1)</script>@mail.com", fake.password(10), id="xss_like_email"),
]


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("email, password", invalid_login_test_data)
def test_login_invalid(shared_page: Application, email: str, password: str):
    shared_page.login_page.open()
    shared_page.login_page.is_loaded()
    shared_page.login_page.login_user(email, password)
    shared_page.login_page.invalid_login_message_visible()
    shared_page.page.wait_for_timeout(2000)


@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(logged_app: Application):
    logged_app.projects_page.is_loaded()
