"""Main application entry point."""
# Application initialization and startup

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers import start, admin, settings, watchlist

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def main():
    """Start the bot."""
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start.start_handler))
    application.add_handler(CommandHandler("admin", admin.admin_handler))
    application.add_handler(CommandHandler("settings", settings.settings_handler))
    application.add_handler(CommandHandler("watchlist", watchlist.watchlist_handler))
    
    # Start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
