from typing import Self

from playwright.sync_api import Page, expect


class ProjectsPageHeader:

    def __init__(self, page: Page):
        self.page = page

        self.page_title = page.locator("h2", has_text="Projects")
        self.company_selector = page.locator("#company_id")
        self.plan_badge = page.locator(".tooltip-project-plan")
        self.enterprise_plan_label = page.get_by_text("Enterprise plan")
        self.free_plan_label = page.get_by_text("Free plan")

        self.search_input = page.locator("#search")

        self.create_button = page.locator("a.common-btn-primary", has_text="Create")
        self.manage_button = page.locator("a.common-btn-secondary", has_text="Manage")

        self.grid_view_button = page.locator("#grid-view")
        self.table_view_button = page.locator("#table-view")

    def search_project(self, query: str) -> Self:
        self.search_input.fill(query)
        return self

    def select_project(self, query: str):
        self.search_input.fill(query)

    def select_company(self, company_name: str):
        self.company_selector.select_option(label=company_name)

    def click_create(self):
        self.create_button.click()

    def click_manage(self):
        self.manage_button.click()

    def switch_to_grid_view(self):
        self.grid_view_button.click()

    def switch_to_table_view(self):
        self.table_view_button.click()

    def get_selected_company(self, expected_value) -> str:
        return expect(self.company_selector.locator('option[selected]')).to_have_text(expected_value)

    def get_plan_name(self, expected_value) -> str:
        return expect(self.plan_badge.locator('span').last).to_have_text(expected_value)

    def is_loaded(self):
        expect(self.page_title).to_have_text("Projects")
        expect(self.company_selector).to_be_visible()
        expect(self.search_input).to_be_visible()
        expect(self.create_button).to_be_visible()
        expect(self.grid_view_button).to_be_visible()
        expect(self.table_view_button).to_be_visible()
