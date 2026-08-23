"""Influencer search and watchlist operations."""

from __future__ import annotations

from typing import Any, Dict, Optional

from database import repositories as repo
from scraper import clean_handle, fetch_following, fetch_profile, fetch_replies


async def search_influencer(raw: str) -> Dict[str, Any]:
    handle = clean_handle(raw)
    if not handle:
        raise ValueError("Enter a valid username (letters, numbers, underscore).")
    return await fetch_profile(handle)


async def watch_influencer(telegram_id: int, raw: str) -> Dict[str, Any]:
    profile = await search_influencer(raw)
    entry = repo.add_to_watchlist(telegram_id, profile["handle"], display_name=profile.get("display_name"), avatar_url=profile.get("avatar_url"), followers_count=profile.get("followers_count"))
    try:
        following = await fetch_following(profile["handle"])
        for row in following:
            event_id = f"follow-base:{profile['handle'].lower()}:{row['followed_user'].lower()}"
            repo.insert_trail_event({**row, "event_id": event_id, "is_new": False, "baseline": True, "telegram_id": telegram_id})
        replies = await fetch_replies(profile["handle"])
        for row in replies:
            repo.insert_trail_event({**row, "telegram_id": telegram_id, "is_new": False})
        repo.touch_watch_scan(profile["handle"])
    except Exception as exc:
        repo.touch_watch_scan(profile["handle"], error=str(exc))
    return {"profile": profile, "entry": entry}


def format_followers(n: Optional[int]) -> str:
    if n is None: return "—"
    if n >= 1_000_000: return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 1_000: return f"{n / 1_000:.1f}K".replace(".0K", "K")
    return str(n)


def watchlist_status_emoji(entry: Dict[str, Any]) -> str:
    if entry.get("paused"): return "⏸"
    if entry.get("last_error"): return "🔴"
    if entry.get("last_scanned_at"): return "🟢"
    return "🟡"
