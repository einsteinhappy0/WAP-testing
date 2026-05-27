"""Twitch search-results page."""
from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from .base_page import BasePage
from .locators.search_results_locators import SearchResultsLocators
from .streamer_page import StreamerPage


class SearchResultsPage(BasePage):
    def search_for(self, term: str) -> "SearchResultsPage":
        locator = self.find_first_present(SearchResultsLocators.SEARCH_INPUT_CHAIN)
        input_field = self.find_visible(locator)
        input_field.clear()
        input_field.send_keys(term)
        input_field.send_keys(Keys.ENTER)
        self.wait_for_document_ready()
        return self

    def open_channels_tab(self) -> "SearchResultsPage":
        """Switch to the Channels tab so live streamer cards are listed.

        The default Top tab often shows only categories and videos — no live
        channels — so we must move to the Channels tab to find a streamer.
        """
        try:
            locator = self.find_first_present(
                SearchResultsLocators.CHANNELS_TAB_CHAIN, per_locator_timeout=3
            )
            self.click(locator)
        except TimeoutException:
            current = self.driver.current_url
            joiner = "&" if "?" in current else "?"
            self.driver.get(current + joiner + "type=channels")
        self.wait_for_document_ready()
        return self

    def scroll_down(self, times: int = 2, pixels: int = 800, pause: float = 1.0) -> "SearchResultsPage":
        for _ in range(times):
            self.scroll_by(pixels)
            time.sleep(pause)  # allow lazy-loaded result cards to render
        return self

    def open_first_streamer(self) -> StreamerPage:
        locator = self.find_first_present(
            SearchResultsLocators.STREAMER_CARD_CHAIN, per_locator_timeout=5
        )
        self.click(locator)
        return StreamerPage(self.driver)
