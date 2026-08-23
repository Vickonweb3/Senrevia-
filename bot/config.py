"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import FrozenSet

from dotenv import load_dotenv

load_dotenv()


def _parse_admin_ids(raw: str) -> FrozenSet[int]:
    ids: set[int] = set()
    for part in (raw or "").replace(";", ",").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.add(int(part))
        except ValueError:
            continue
    return frozenset(ids)


class Settings:
    """Runtime settings for Senrivia."""

    def __init__(self) -> None:
        self.bot_token: str = os.getenv("BOT_TOKEN", "").strip()
        self.admin_ids: FrozenSet[int] = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))
        self.mongodb_uri: str = os.getenv("MONGODB_URI", "").strip()
        self.mongodb_db: str = os.getenv("MONGODB_DB", "senrivia").strip() or "senrivia"
        self.admin_host: str = os.getenv("ADMIN_HOST", "0.0.0.0").strip() or "0.0.0.0"
        self.admin_port: int = int(os.getenv("ADMIN_PORT", "8090") or "8090")
        self.admin_secret: str = os.getenv("ADMIN_SECRET", "").strip()
        self.scrape_interval_minutes: int = max(
            5, int(os.getenv("SCRAPE_INTERVAL_MINUTES", "15") or "15")
        )
        self.admin_public_url: str = os.getenv("ADMIN_PUBLIC_URL", "").strip().rstrip("/")

    def validate(self) -> None:
        missing = []
        if not self.bot_token:
            missing.append("BOT_TOKEN")
        if not self.mongodb_uri:
            missing.append("MONGODB_URI")
        if missing:
            raise RuntimeError(
                "Missing required environment variables: " + ", ".join(missing)
            )

    def is_admin(self, user_id: int | None) -> bool:
        if user_id is None:
            return False
        return int(user_id) in self.admin_ids


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
