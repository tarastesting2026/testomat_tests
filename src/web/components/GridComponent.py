from playwright.sync_api import Page, Locator

from src.web.components.ProjectCard import ProjectCard


class GridComponent:
    def __init__(self, page: Page):
        self.page = page
        self.root: Locator = page.locator("#grid")
        self.cards: Locator = self.root.locator("ul > li")

    def get_all_cards(self) -> list[ProjectCard]:
        return [ProjectCard(card) for card in self.cards.all()]

    def get_demo_cards(self) -> list[ProjectCard]:
        return [
            ProjectCard(card)
            for card in self.cards.all()
            if "Demo" in (card.locator(".project-badges").text_content() or "")
        ]

    def get_card_by_name(self, name: str) -> ProjectCard:
        card = self.cards.filter(has_text=name).first
        return ProjectCard(card)

    def count(self) -> int:
        return self.cards.count()

    def get_card_by_title(self, title: str) -> ProjectCard:
        card = self.root.locator(
            "li", has=self.page.locator(f"h3:text('{title}')")
        )
        return ProjectCard(card)
