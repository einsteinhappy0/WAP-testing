"""Twitch home page."""
from __future__ import annotations

from selenium.common.exceptions import TimeoutException

from .base_page import BasePage
from .locators.home_locators import HomeLocators
from .search_results_page import SearchResultsPage


class HomePage(BasePage):
    URL = "https://m.twitch.tv/"
    SEARCH_URL = "https://m.twitch.tv/search"

    def open(self) -> "HomePage":
        self.driver.get(self.URL)
        self.wait_for_document_ready()
        return self

    def open_search(self) -> SearchResultsPage:
        # Click the search icon if one is present; otherwise navigate directly.
        # The mobile home page currently renders no search entry-point, so the
        # URL fallback is the common path.
        try:
            locator = self.find_first_present(
                HomeLocators.SEARCH_ICON_CHAIN, per_locator_timeout=2
            )
            self.click(locator)
        except TimeoutException:
            self.driver.get(self.SEARCH_URL)
            self.wait_for_document_ready()
        return SearchResultsPage(self.driver)
