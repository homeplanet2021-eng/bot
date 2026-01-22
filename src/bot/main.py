"""Bot entrypoint placeholder with preflight checks."""

from __future__ import annotations

import sys

import httpx

from bot.config import AppConfig


def preflight_check(panel_url: str) -> None:
    try:
        response = httpx.get(panel_url, timeout=5.0)
        response.raise_for_status()
    except Exception as exc:  # noqa: BLE001 - surface actionable error
        message = (
            "Remnawave preflight failed. "
            f"Ensure {panel_url} is reachable inside remnawave-network."
        )
        raise RuntimeError(message) from exc


def main() -> int:
    config = AppConfig.load()
    if not config.remnawave_panel_url:
        print("REMNAWAVE_PANEL_URL is required.")
        return 1
    preflight_check(config.remnawave_panel_url)
    print("Bot preflight OK. TODO: start aiogram app.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
