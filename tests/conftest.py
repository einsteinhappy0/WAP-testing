"""Shared pytest fixtures: WebDriver lifecycle + screenshot directory."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

SCREENSHOT_DIR = Path(__file__).resolve().parents[1] / "screenshots"

# Emulate a mobile device — Twitch's m.* site is more locator-stable for this scenario.
# Explicit metrics + UA (ChromeDriver's built-in device-name list is unstable across versions).
_MOBILE_EMULATION = {
    "deviceMetrics": {"width": 412, "height": 915, "pixelRatio": 2.625},
    "userAgent": (
        "Mozilla/5.0 (Linux; Android 13; Pixel 5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/148.0.0.0 Mobile Safari/537.36"
    ),
}


def _build_chrome_options() -> Options:
    options = Options()
    options.add_experimental_option("mobileEmulation", _MOBILE_EMULATION)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-US")
    if os.getenv("HEADLESS"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=412,915")
    return options


@pytest.fixture(scope="session", autouse=True)
def _ensure_screenshot_dir() -> None:
    SCREENSHOT_DIR.mkdir(exist_ok=True)


@pytest.fixture
def driver() -> Iterator[webdriver.Chrome]:
    chrome = webdriver.Chrome(options=_build_chrome_options())
    chrome.set_page_load_timeout(60)
    try:
        yield chrome
    finally:
        chrome.quit()


@pytest.fixture
def screenshot_dir() -> Path:
    return SCREENSHOT_DIR
