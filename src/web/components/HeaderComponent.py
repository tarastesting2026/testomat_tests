from playwright.sync_api import Locator


class HeaderComponent:

    def __init__(self, root: Locator):
        self.root = root
        self.title = root.locator("h2")
        self.company_select = root.locator("#company_id")
        self.search_input = root.locator("#search")
        self.create_button = root.get_by_role("link", name="Create")
        self.grid_view_button = root.locator("#grid-view")
        self.table_view_button = root.locator("#table-view")
        self.plan_badge = root.locator(".tooltip-project-plan span").last

    def search(self, text: str):
        self.search_input.fill(text)

    def select_company(self, value: str):
        self.company_select.select_option(value)

    def click_create(self):
        self.create_button.click()

    def switch_to_table_view(self):
        self.table_view_button.click()

    def switch_to_grid_view(self):
        self.grid_view_button.click()
