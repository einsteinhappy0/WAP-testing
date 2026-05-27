# WAP — Twitch Automation

Selenium + pytest UI tests for Twitch, using the Page Object Model.

The scenario emulates a mobile device, searches for *StarCraft II*, opens a streamer,
dismisses any mature-content modal, waits for the video to load, and takes a screenshot.

## Setup

```bash
uv sync           # or: pip install -e .
```

A local Chrome / Chromium installation is required. The driver is resolved
automatically via `webdriver-manager`.

## Run

```bash
pytest                                  # headed
HEADLESS=1 pytest                       # headless
pytest tests/test_twitch_search.py -k starcraft
```

Screenshots are written to `./screenshots/`.

## Layout

```
pages/         Page Objects (one class per page)
  base_page.py
  home_page.py
  search_results_page.py
  streamer_page.py
tests/         pytest test cases
  conftest.py  WebDriver fixture
  test_twitch_search.py
```

# Test Steps:
1. go to Twitch
2. click the search icon
3. input "StarCraft II"
4. scroll down 2 times
5. select one streamer
6. on the streamer page wait until everything loads and take a screenshot
7. handle any pre-roll modal / pop-up that appears before the video loads
