from playwright.sync_api import Page, Locator, expect

from src.web.components.GridComponent import GridComponent
from src.web.components.HeaderComponent import HeaderComponent
from src.web.components.ProjectCard import ProjectCard


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

        self.header = HeaderComponent(page)

        self.grid = GridComponent(page)

        self.project_cards = page.locator("#grid ul > li")

        self.project_cards: Locator = page.locator("#grid ul > li")

    def is_loaded(self):
        expect(self.page.locator("h2")).to_have_text("Projects")
        expect(self.project_cards.first).to_be_visible()

    def projects_not_empty(self):
        expect(self.project_cards).not_to_have_count(0)

    def projects_count_is(self, count: int):
        expect(self.visible_project_cards()).to_have_count(count)

    def get_all_projects(self) -> list[ProjectCard]:
        return [
            ProjectCard(card)
            for card in self.project_cards.all()
        ]

    def get_project_by_index(self, index: int) -> ProjectCard:
        return ProjectCard(self.project_cards.nth(index))

    def get_project_by_name(self, name: str) -> ProjectCard:
        card = self.project_cards.filter(
            has=self.page.locator("h3", has_text=name)
        ).first
        return ProjectCard(card)

    def search_project(self, name: str):
        self.header.search_input.fill(name)

    def open_project(self, name: str):
        self.get_project_by_name(name).open()

    def project_visible(self, name: str):
        expect(
            self.page.get_by_role("heading", name=name)
        ).to_be_visible()

    def project_hidden(self, name: str):
        expect(
            self.page.get_by_role("heading", name=name)
        ).to_be_hidden()

    def project_has_badges(self, name: str):
        card = self.get_project_by_name(name)
        expect(card.badges).not_to_have_count(0)

    def project_tests_count_contains(self, name: str, text: str):
        card = self.get_project_by_name(name)
        expect(card.tests_count).to_contain_text(text)

    def visible_project_cards(self) -> Locator:
        return self.project_cards.filter(
            has=self.page.locator("h3:visible")
        )
