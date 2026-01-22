"""Configuration loader for the bot."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    telegram_bot_token: str
    telegram_webhook_public_url: str
    telegram_webhook_secret_token: str
    admin_tg_ids: str
    enable_stars_autorenewal: bool
    remnawave_panel_url: str
    remnawave_api_token: str
    remnawave_panel_version: str
    remnawave_contract_version: str
    env: str
    safe_mode: bool
    tz: str
    database_url: str
    redis_url: str


    @staticmethod
    def _get_bool(name: str, default: bool) -> bool:
        value = os.getenv(name)
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}


    @classmethod
    def load(cls) -> "AppConfig":
        return cls(
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            telegram_webhook_public_url=os.getenv("TELEGRAM_WEBHOOK_PUBLIC_URL", ""),
            telegram_webhook_secret_token=os.getenv("TELEGRAM_WEBHOOK_SECRET_TOKEN", ""),
            admin_tg_ids=os.getenv("ADMIN_TG_IDS", ""),
            enable_stars_autorenewal=cls._get_bool("ENABLE_STARS_AUTORENEWAL", False),
            remnawave_panel_url=os.getenv("REMNAWAVE_PANEL_URL", ""),
            remnawave_api_token=os.getenv("REMNAWAVE_API_TOKEN", ""),
            remnawave_panel_version=os.getenv("REMNAWAVE_PANEL_VERSION", ""),
            remnawave_contract_version=os.getenv("REMNAWAVE_CONTRACT_VERSION", ""),
            env=os.getenv("ENV", "development"),
            safe_mode=cls._get_bool("SAFE_MODE", True),
            tz=os.getenv("TZ", "UTC"),
            database_url=os.getenv("DATABASE_URL", ""),
            redis_url=os.getenv("REDIS_URL", ""),
        )
