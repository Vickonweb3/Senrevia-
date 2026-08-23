#!/usr/bin/env python3
"""Senrivia entrypoint — Telegram bot + optional admin dashboard."""

from __future__ import annotations

import logging
import threading

import uvicorn

from admin.dashboard import create_admin_app
from bot.app import build_application
from bot.config import get_settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
log = logging.getLogger("senrivia")


def run_admin() -> None:
    settings = get_settings()
    if not settings.admin_secret:
        log.warning("ADMIN_SECRET empty — admin dashboard will reject all requests until set")
    app = create_admin_app()
    uvicorn.run(app, host=settings.admin_host, port=settings.admin_port, log_level="info")


def main() -> None:
    settings = get_settings()
    settings.validate()
    t = threading.Thread(target=run_admin, name="senrivia-admin", daemon=True)
    t.start()
    log.info("Admin dashboard on http://%s:%s", settings.admin_host, settings.admin_port)
    application = build_application()
    log.info("Starting Telegram polling…")
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
