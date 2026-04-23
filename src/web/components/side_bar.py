import re

from playwright.sync_api import Page, Locator, expect


class SideBar:

    def __init__(self, page: Page):
        self.page = page

        self._menu = page.locator(".mainnav-menu")
        self._logo = page.locator("button.btn-open")
        self._close_button = page.get_by_role("button", name="Close")
        self._tests_link = page.get_by_role("link", name="Tests")
        self._runs_link = page.get_by_role("link", name="Runs")
        self._requirements_link = page.get_by_role("link", name="Requirements")
        self._plans_link = page.get_by_role("link", name="Plans")
        self._steps_link = page.get_by_role("link", name="Steps")
        self._pulse_link = page.get_by_role("link", name="Pulse")
        self._imports_link = page.get_by_role("link", name="Imports")
        self._analytics_link = page.get_by_role("link", name="Analytics")
        self._branches_link = page.get_by_role("link", name="Branches")
        self._settings_link = page.get_by_role("link", name="Settings")
        self._help_link = page.get_by_role("link", name="Help")
        self._projects_link = page.get_by_role("link", name="Projects")
        self._profile_link = page.get_by_role("link", name="taras.testing.2026")

    def is_loaded(self) -> SideBar:
        expect(self._menu).to_be_visible()
        expect(self._logo).to_be_visible()
        return self

    def go_to_tests(self) -> None:
        self._tests_link.click()

    def go_to_requirements(self) -> None:
        self._requirements_link.click()

    def go_to_runs(self) -> None:
        self._runs_link.click()

    def go_to_plans(self) -> None:
        self._plans_link.click()

    def go_to_steps(self) -> None:
        self._steps_link.click()

    def go_to_pulse(self) -> None:
        self._pulse_link.click()

    def go_to_imports(self) -> None:
        self._imports_link.click()

    def go_to_analytics(self) -> None:
        self._analytics_link.click()

    def go_to_branches(self) -> None:
        self._branches_link.click()

    def go_to_settings(self) -> None:
        self._settings_link.click()

    def go_to_projects(self) -> None:
        self._projects_link.click()

    def open_help(self) -> None:
        self._help_link.click()

    def open_profile(self) -> None:
        self._profile_link.click()

    def collapse_sidebar(self) -> None:
        self._close_button.click()

    def is_link_active(self, link: Locator) -> bool:
        return "active" in (link.get_attribute("class") or "")

    def is_link_disabled(self, link: Locator) -> bool:
        label = link.locator(".label-container")
        return "opacity-50" in (label.get_attribute("class") or "")

    def active_nav_item(self) -> Locator:
        return self.page.locator("a.active.nav-item")

    def get_username(self) -> str:
        return (
            self._profile_link
            .locator(".label-container")
            .inner_text()
            .strip()
        )

    def click_logo(self) -> SideBar:
        self._logo.click()
        return self

    def close_menu(self) -> SideBar:
        self._close_button.click()
        return self

    def get_user_profile_link(self, username: str):
        return self.page.get_by_role("link", name=username)

    def get_user_profile(self, username: str) -> SideBar:
        self.get_user_profile_link(username).click()
        return self

    def link_by_name(self, name: str):
        return self._menu.get_by_role("link", name=name)

    def expect_tab_active(self, name: str) -> SideBar:
        link = self.link_by_name(name)
        expect(link).to_be_visible()
        expect(link).to_have_class(re.compile(r"\bactive\b"))
        return self
