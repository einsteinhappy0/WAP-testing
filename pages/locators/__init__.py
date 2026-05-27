"""Centralised element locators.

Each page has its own locator module. Locators are ordered tuples of
``(By, selector)`` pairs and grouped into ``Locator`` lists where multiple
strategies are acceptable — callers should try them in order and pick the
first one that resolves.

Selector preference (most → least stable):

1. ``data-a-target`` / ``data-test-selector`` — Twitch's own automation hooks.
2. ``aria-label`` / ``role`` — semantic, i18n-tolerant, ships in the DOM.
3. Stable HTML attributes (``type``, ``href`` prefix, tag name).
4. Structural CSS — last resort only.

Hashed CSS-module class names (``class*='ScSomething-sc-xxxxx-0'``) are
deliberately avoided because they churn on every Twitch build.
"""
from __future__ import annotations

from typing import Tuple

Locator = Tuple[str, str]
