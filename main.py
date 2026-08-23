"""Main application entry point."""

import logging

from telegram.ext import Application, CommandHandler

from bot.config import get_settings
from bot.handlers import admin, settings, start, watchlist

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the Telegram bot."""
    config = get_settings()
    config.validate()

    application = Application.builder().token(config.bot_token).build()

    application.add_handler(CommandHandler("start", start.start_handler))
    application.add_handler(CommandHandler("admin", admin.admin_handler))
    application.add_handler(CommandHandler("broadcast", admin.broadcast_handler))
    application.add_handler(CommandHandler("settings", settings.settings_handler))
    application.add_handler(CommandHandler("watchlist", watchlist.watchlist_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
