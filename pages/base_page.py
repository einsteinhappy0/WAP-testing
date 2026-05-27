"""Base Page Object: shared waiting / interaction helpers."""
from __future__ import annotations

from typing import Iterable

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .locators import Locator


class BasePage:
    DEFAULT_TIMEOUT = 20

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self._driver = driver
        self._timeout = timeout

    @property
    def driver(self) -> WebDriver:
        return self._driver

    def _wait(self, timeout: int | None = None) -> WebDriverWait:
        return WebDriverWait(self._driver, timeout or self._timeout)

    def find_visible(self, locator: Locator, timeout: int | None = None) -> WebElement:
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def is_present(self, locator: Locator, timeout: int = 3) -> bool:
        try:
            self._wait(timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def find_first_present(
        self,
        locators: Iterable[Locator],
        per_locator_timeout: int = 3,
    ) -> Locator:
        """Return the first locator from ``locators`` that resolves in the DOM.

        Letting callers store an ordered chain of locators per element makes
        the test resilient to A/B variants and DOM refactors.
        """
        last_error: Exception | None = None
        for locator in locators:
            if self.is_present(locator, timeout=per_locator_timeout):
                return locator
            last_error = TimeoutException(f"Locator not present: {locator}")
        raise last_error or TimeoutException("No locators provided")

    def click(self, locator: Locator, timeout: int | None = None) -> None:
        element = self._wait(timeout).until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            self._driver.execute_script("arguments[0].click();", element)

    def scroll_by(self, pixels: int) -> None:
        self._driver.execute_script("window.scrollBy(0, arguments[0]);", pixels)

    def wait_for_document_ready(self, timeout: int | None = None) -> None:
        self._wait(timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def take_screenshot(self, path: str) -> None:
        self._driver.save_screenshot(path)
