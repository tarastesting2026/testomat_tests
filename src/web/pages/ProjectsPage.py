from playwright.sync_api import Page, Locator, expect

from src.web.components.ProjectCard import ProjectCard
from src.web.components.ProjectsPageHeader import ProjectsPageHeader


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = ProjectsPageHeader(page)

        self.success_message = page.locator(".common-flash-success-right p")
        self.info_message = page.locator(".common-flash-info-right p")

        self.projects_grid = page.locator("#grid")
        self.project_cards = page.locator("#grid ul > li")

        self.total_count = page.locator(".common-counter")
        self.page_heading = page.locator(".common-page-header h2")

    def is_loaded(self):
        expect(self.page.locator("h2")).to_have_text("Projects")
        expect(self.project_cards.first).to_be_visible()

    def verify_page_loaded(self):
        expect(self.header.page_title).to_be_visible()
        expect(self.projects_grid).to_be_visible()

    def verify_success_message(self, expected_text: str):
        expect(self.success_message).to_have_text(expected_text)

    def get_demo_projects(self) -> list[ProjectCard]:
        return [project for project in self.get_projects() if project.is_demo()]

    def is_demo_project(self):
        return self.project_has_badges("Demo")

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

    def navigate(self, url: str = '/projects'):
        self.page.goto(url)
        self.page_heading.wait_for(state='visible')

    def get_success_message(self) -> str:
        return self.success_message.text_content().strip()

    def get_projects(self) -> list[ProjectCard]:
        return [ProjectCard(card) for card in self.project_cards.all()]

    def get_project_by_title(self, title: str) -> ProjectCard:
        card = self.project_cards.filter(has=self.page.locator("h3", has_text=title)).first
        return ProjectCard(card)

    def count_of_project_visibility(self, expected_count: int):
        return expect(self.project_cards.filter(visible=True)).to_have_count(expected_count)
