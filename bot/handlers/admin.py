"""Admin command handlers."""

import asyncio
import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_settings
from bot.services.users import get_user_registry

logger = logging.getLogger(__name__)


async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the admin menu."""
    settings = get_settings()
    if not settings.is_admin(update.effective_user.id if update.effective_user else None):
        await update.effective_message.reply_text("You are not authorized to use admin commands.")
        return

    await update.effective_message.reply_text(
        "Admin panel\n\n"
        "Broadcast to all registered users:\n"
        "/broadcast Your message here"
    )


async def broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast a text message to every registered Telegram chat."""
    settings = get_settings()
    if not settings.is_admin(update.effective_user.id if update.effective_user else None):
        await update.effective_message.reply_text("You are not authorized to use admin commands.")
        return

    message = " ".join(context.args).strip()
    if not message:
        await update.effective_message.reply_text(
            "Usage: /broadcast Your message here"
        )
        return

    chat_ids = get_user_registry().chat_ids()
    sent = failed = 0

    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
            sent += 1
        except Exception as exc:
            failed += 1
            logger.warning("Broadcast failed for chat %s: %s", chat_id, exc)
        await asyncio.sleep(0.05)

    await update.effective_message.reply_text(
        f"Broadcast complete.\nSent: {sent}\nFailed: {failed}"
    )
