from __future__ import annotations

from pathlib import Path

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
def test_search_starcraft_ii_and_open_streamer(driver, screenshot_dir: Path) -> None:
    streamer_page = (
        HomePage(driver)
        .open()
        .open_search()
        .search_for("StarCraft II")
        .open_channels_tab()
        .scroll_down(times=2)
        .open_first_streamer()
    )

    streamer_page.dismiss_pre_roll_modals().wait_until_loaded()

    screenshot_path = screenshot_dir / "starcraft_streamer.png"
    streamer_page.take_screenshot(str(screenshot_path))

    assert screenshot_path.exists(), f"Screenshot was not written to {screenshot_path}"
    assert screenshot_path.stat().st_size > 0, "Screenshot file is empty"
