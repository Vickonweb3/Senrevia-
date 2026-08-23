"""Data access layer for Senrivia collections."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo import ReturnDocument

from .mongo import get_db


def _now() -> datetime:
    return datetime.now(timezone.utc)


def upsert_user(telegram_id: int, *, username: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, language_code: Optional[str] = None) -> Dict[str, Any]:
    db = get_db()
    update = {"$set": {"username": username, "first_name": first_name, "last_name": last_name, "language_code": language_code, "last_active_at": _now()}, "$setOnInsert": {"telegram_id": telegram_id, "joined_at": _now(), "is_blocked": False, "settings": {"alerts_enabled": True, "quiet_hours": False}}, "$inc": {"interaction_count": 1}}
    return db.users.find_one_and_update({"telegram_id": telegram_id}, update, upsert=True, return_document=ReturnDocument.AFTER)


def get_user(telegram_id: int) -> Optional[Dict[str, Any]]: return get_db().users.find_one({"telegram_id": telegram_id})
def count_users() -> int: return get_db().users.count_documents({})
def list_users(limit: int = 50, skip: int = 0) -> List[Dict[str, Any]]: return list(get_db().users.find().sort("joined_at", -1).skip(skip).limit(limit))


def add_to_watchlist(telegram_id: int, handle: str, *, display_name: Optional[str] = None, avatar_url: Optional[str] = None, followers_count: Optional[int] = None) -> Dict[str, Any]:
    db = get_db(); handle_clean = handle.lstrip("@").strip()
    doc = {"telegram_id": telegram_id, "handle": handle_clean, "handle_lower": handle_clean.lower(), "display_name": display_name or handle_clean, "avatar_url": avatar_url, "followers_count": followers_count, "paused": False, "added_at": _now(), "last_scanned_at": None, "last_error": None}
    existing = db.watchlist.find_one({"telegram_id": telegram_id, "handle_lower": handle_clean.lower()})
    if existing: return existing
    db.watchlist.insert_one(doc); return doc


def remove_from_watchlist(telegram_id: int, handle: str) -> bool:
    result = get_db().watchlist.delete_one({"telegram_id": telegram_id, "handle_lower": handle.lstrip("@").lower()}); return result.deleted_count > 0


def set_watch_paused(telegram_id: int, handle: str, paused: bool) -> Optional[Dict[str, Any]]:
    return get_db().watchlist.find_one_and_update({"telegram_id": telegram_id, "handle_lower": handle.lstrip("@").lower()}, {"$set": {"paused": paused, "updated_at": _now()}}, return_document=ReturnDocument.AFTER)


def list_watchlist(telegram_id: int) -> List[Dict[str, Any]]: return list(get_db().watchlist.find({"telegram_id": telegram_id}).sort("added_at", -1))

def list_active_watch_handles() -> List[str]:
    pipeline = [{"$match": {"paused": False}}, {"$group": {"_id": "$handle_lower", "handle": {"$first": "$handle"}}}, {"$sort": {"handle": 1}}]
    return [row["handle"] for row in get_db().watchlist.aggregate(pipeline)]

def users_tracking_handle(handle: str, *, active_only: bool = True) -> List[int]:
    query: Dict[str, Any] = {"handle_lower": handle.lstrip("@").lower()}
    if active_only: query["paused"] = False
    return [doc["telegram_id"] for doc in get_db().watchlist.find(query, {"telegram_id": 1})]

def count_watchlist_entries() -> int: return get_db().watchlist.count_documents({})
def count_active_watches() -> int: return get_db().watchlist.count_documents({"paused": False})


def insert_trail_event(event: Dict[str, Any]) -> bool:
    db = get_db(); event = dict(event); event.setdefault("created_at", _now())
    try: db.trails.insert_one(event); return True
    except Exception: return False


def list_trails_for_user(telegram_id: int, limit: int = 20) -> List[Dict[str, Any]]:
    handles = [w["handle_lower"] for w in list_watchlist(telegram_id)]
    if not handles: return []
    return list(get_db().trails.find({"handle_lower": {"$in": handles}}).sort("created_at", -1).limit(limit))

def list_trails_for_handle(handle: str, limit: int = 20) -> List[Dict[str, Any]]: return list(get_db().trails.find({"handle_lower": handle.lstrip("@").lower()}).sort("created_at", -1).limit(limit))
def count_trails() -> int: return get_db().trails.count_documents({})

def update_user_settings(telegram_id: int, settings: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return get_db().users.find_one_and_update({"telegram_id": telegram_id}, {"$set": {f"settings.{k}": v for k, v in settings.items()}, "last_active_at": _now()}, return_document=ReturnDocument.AFTER)

def log_scrape(message: str, *, level: str = "info", handle: Optional[str] = None) -> None: get_db().scrape_log.insert_one({"level": level, "message": message, "handle": handle, "created_at": _now()})

def admin_stats() -> Dict[str, Any]:
    db = get_db(); recent_users = list(db.users.find().sort("joined_at", -1).limit(10)); top_tracked = list(db.watchlist.aggregate([{"$group": {"_id": "$handle_lower", "handle": {"$first": "$handle"}, "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 10}]))
    return {"users_total": db.users.count_documents({}), "watch_total": db.watchlist.count_documents({}), "watch_active": db.watchlist.count_documents({"paused": False}), "watch_paused": db.watchlist.count_documents({"paused": True}), "trails_total": db.trails.count_documents({}), "recent_users": recent_users, "top_tracked": top_tracked}

def touch_watch_scan(handle: str, *, error: Optional[str] = None) -> None:
    get_db().watchlist.update_many({"handle_lower": handle.lstrip("@").lower()}, {"$set": {"last_scanned_at": _now(), "last_error": error}})
