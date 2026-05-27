"""Twitch streamer (channel) page."""
from __future__ import annotations

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)

from .base_page import BasePage
from .locators.streamer_locators import StreamerLocators


class StreamerPage(BasePage):
    def dismiss_pre_roll_modals(self) -> "StreamerPage":
        """Best-effort dismissal of any pop-ups that gate the video player."""
        for locator in StreamerLocators.PRE_ROLL_DISMISS_CHAIN:
            if self.is_present(locator, timeout=3):
                try:
                    self.click(locator, timeout=3)
                except (TimeoutException, ElementClickInterceptedException):
                    pass
        return self

    def wait_until_loaded(self, timeout: int = 30) -> "StreamerPage":
        self.wait_for_document_ready(timeout=timeout)
        # Channel chrome (follow button etc.) usually mounts before the player.
        self.find_visible(StreamerLocators.CHANNEL_CHROME, timeout=timeout)
        self.find_visible(StreamerLocators.PLAYER_ROOT, timeout=timeout)
        self.find_visible(StreamerLocators.VIDEO, timeout=timeout)
        return self
