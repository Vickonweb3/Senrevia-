"""MongoDB-backed Telegram user registry used by admin broadcasts."""

from __future__ import annotations

from datetime import datetime, timezone

from pymongo import MongoClient

from bot.config import get_settings


class UserRegistry:
    """Store Telegram chat IDs that have started the bot."""

    def __init__(self) -> None:
        settings = get_settings()
        self._client = MongoClient(settings.mongodb_uri)
        self._collection = self._client[settings.mongodb_db]["users"]

    def register(self, user, chat_id: int) -> None:
        now = datetime.now(timezone.utc)
        self._collection.update_one(
            {"chat_id": int(chat_id)},
            {
                "$set": {
                    "chat_id": int(chat_id),
                    "user_id": int(user.id),
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "updated_at": now,
                },
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )

    def chat_ids(self):
        return self._collection.distinct("chat_id")


_registry: UserRegistry | None = None


def get_user_registry() -> UserRegistry:
    global _registry
    if _registry is None:
        _registry = UserRegistry()
    return _registry
