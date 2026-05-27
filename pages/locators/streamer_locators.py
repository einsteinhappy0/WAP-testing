"""Locators for the Twitch streamer (channel) page (mobile)."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from . import Locator


def _ci_text(needle: str) -> str:
    """Case-insensitive XPath text-contains predicate body."""
    lower = needle.lower()
    return (
        "contains(translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        f"'{lower}')"
    )


class StreamerLocators:
    # ---- "Player is mounted" signals ---------------------------------------
    # Canonical: the <video> element. Present once the player initialises.
    VIDEO: Locator = (By.CSS_SELECTOR, "video")
    # Player root container — mounted before <video> in most cases.
    PLAYER_ROOT: Locator = (
        By.CSS_SELECTOR,
        "div[data-a-target='video-player'], div[data-a-player-state], "
        "div[class*='video-player__default-player']",
    )

    # ---- "Channel page chrome loaded" signal -------------------------------
    # The follow button is the most reliable channel-loaded indicator on
    # m.twitch.tv right now (verified 2026-05). The older 'channel-header' /
    # 'stream-title' hooks are no longer present on mobile.
    CHANNEL_CHROME: Locator = (
        By.CSS_SELECTOR,
        "button[data-a-target='follow-button'], "
        "[data-a-target='channel-header'], "
        "[data-a-target='stream-title']",
    )

    # ---- Pre-roll / interstitial modals ------------------------------------
    # 1) "Open in App" mobile interstitial — the most common gate on m.twitch.tv.
    #    The dialog's "Continue on web" button is text-based; we cover the
    #    common locales.
    CONTINUE_ON_WEB_BUTTON: Locator = (
        By.XPATH,
        f"//div[@role='dialog']//button[{_ci_text('continue on web')} "
        f"or {_ci_text('繼續使用網頁版')} "
        f"or {_ci_text('continuar en la web')} "
        f"or {_ci_text('웹에서 계속')} "
        f"or {_ci_text('continuer sur le web')}]",
    )
    # 2) Mature-content / classification gate.
    MATURE_CONTENT_ACCEPT: Locator = (
        By.CSS_SELECTOR,
        "button[data-a-target='player-overlay-mature-accept'], "
        "button[data-a-target='content-classification-gate-overlay-start-watching-button']",
    )
    # 3) Generic "Start Watching" gate (intro / classification overlay).
    START_WATCHING_BUTTON: Locator = (
        By.XPATH,
        f"//button[{_ci_text('start watching')} or {_ci_text('開始觀看')}]",
    )
    # 4) Cookie / consent banner — text-based; the DOM hook varies by region.
    CONSENT_ACCEPT_BUTTON: Locator = (
        By.XPATH,
        f"//button[{_ci_text('accept')} or {_ci_text('agree')} "
        f"or {_ci_text('同意')} or {_ci_text('接受')}]",
    )
    # 5) Generic dialog close (X / Dismiss) — last-resort dismissal.
    MODAL_CLOSE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "div[role='dialog'] button[aria-label*='Close' i], "
        "div[role='dialog'] button[aria-label*='關閉' i], "
        "button[data-a-target='modal-close-button'], "
        "button[aria-label='Dismiss' i]",
    )

    # Try in this order: known player gates first, then app interstitial,
    # then consent, then generic close.
    PRE_ROLL_DISMISS_CHAIN: tuple[Locator, ...] = (
        MATURE_CONTENT_ACCEPT,
        START_WATCHING_BUTTON,
        CONTINUE_ON_WEB_BUTTON,
        CONSENT_ACCEPT_BUTTON,
        MODAL_CLOSE_BUTTON,
    )
