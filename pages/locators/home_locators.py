"""Locators for the Twitch mobile home page.

The current m.twitch.tv layout renders no search icon, so HomePage.open_search
falls back to navigating directly to /search when this chain misses. The chain
stays defined so a re-introduced icon would be picked up first.
"""
from __future__ import annotations

from selenium.webdriver.common.by import By

from . import Locator


class HomeLocators:
    SEARCH_ICON_PRIMARY: Locator = (By.CSS_SELECTOR, "a[data-a-target='search-button']")
    SEARCH_ICON_BY_HREF: Locator = (
        By.CSS_SELECTOR,
        "a[href='/search'], a[href^='/search?'], a[href^='/search/']",
    )
    SEARCH_ICON_BY_ARIA: Locator = (
        By.CSS_SELECTOR,
        "a[aria-label='Search' i], button[aria-label='Search' i], "
        "a[aria-label*='搜尋' i], button[aria-label*='搜尋' i]",
    )

    SEARCH_ICON_CHAIN: tuple[Locator, ...] = (
        SEARCH_ICON_PRIMARY,
        SEARCH_ICON_BY_HREF,
        SEARCH_ICON_BY_ARIA,
    )
