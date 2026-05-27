"""Locators for the Twitch search-results page (mobile)."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from . import Locator


class SearchResultsLocators:
    SEARCH_INPUT_PRIMARY: Locator = (By.CSS_SELECTOR, "input[data-a-target='tw-input']")
    SEARCH_INPUT_BY_TYPE: Locator = (By.CSS_SELECTOR, "input[type='search']")
    SEARCH_INPUT_BY_ARIA: Locator = (
        By.CSS_SELECTOR,
        "input[aria-label*='Search' i], input[aria-label*='搜尋' i]",
    )

    SEARCH_INPUT_CHAIN: tuple[Locator, ...] = (
        SEARCH_INPUT_PRIMARY,
        SEARCH_INPUT_BY_TYPE,
        SEARCH_INPUT_BY_ARIA,
    )

    CHANNELS_TAB_BY_HREF: Locator = (By.CSS_SELECTOR, "a[role='tab'][href*='type=channels']")
    CHANNELS_TAB_BY_TEXT: Locator = (
        By.XPATH,
        "//a[@role='tab'][contains(normalize-space(.),'Channels') "
        "or contains(normalize-space(.),'頻道') "
        "or contains(normalize-space(.),'チャンネル') "
        "or contains(normalize-space(.),'채널')]",
    )
    CHANNELS_TAB_CHAIN: tuple[Locator, ...] = (
        CHANNELS_TAB_BY_HREF,
        CHANNELS_TAB_BY_TEXT,
    )

    # The mobile site doesn't wrap channel cards in an <a> — the card div carries
    # a click handler — but every card contains a viewer-count line ("觀眾人數" /
    # "viewers"), so we anchor on that to skip offline-channel cards that appear
    # below the live results and would lead to a player-less page.
    STREAMER_CARD_BY_DATA_A_TARGET: Locator = (
        By.CSS_SELECTOR,
        "a[data-a-target='preview-card-image-link'], "
        "a[data-a-target='search-result-live-channel'], "
        "a[data-a-target='search-result-channel']",
    )
    STREAMER_CARD_LIVE_BY_H2: Locator = (
        By.XPATH,
        "//main//h2[not(ancestor::*[@role='tablist']) "
        "and string-length(normalize-space(.))>0 "
        "and not(starts-with(normalize-space(.),'搜尋')) "
        "and not(starts-with(normalize-space(.),'Search')) "
        "and ancestor::*[contains(.,'觀眾人數') or contains(translate(.,"
        "'VIEWERS','viewers'),'viewers')]]",
    )

    STREAMER_CARD_CHAIN: tuple[Locator, ...] = (
        STREAMER_CARD_BY_DATA_A_TARGET,
        STREAMER_CARD_LIVE_BY_H2,
    )
