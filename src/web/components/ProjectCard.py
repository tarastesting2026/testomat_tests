from playwright.sync_api import Locator


class ProjectCard:

    def __init__(self, card_locator: Locator):
        self.root = card_locator
        self.title = card_locator.locator("h3")
        self.tests_count = card_locator.locator("p").filter(has_text="tests")
        self.link = card_locator.locator(":scope > a")
        self.avatars = card_locator.locator(".inline-flex img")
        self.extra_count = card_locator.locator(".inline-flex div").filter(has_text="+")
        self.badges = card_locator.locator(".project-badges .common-badge")

    def get_title(self) -> str:
        return (self.title.text_content() or "").strip()

    def get_tests_count(self) -> str:
        return (self.tests_count.text_content() or "").strip()

    def get_badge_labels(self) -> list[str]:
        return [label.strip() for label in self.badges.all_text_contents()]

    def has_badge(self, label: str) -> bool:
        return any(l.lower() == label.lower() for l in self.get_badge_labels())

    def open(self) -> None:
        self.link.click()
