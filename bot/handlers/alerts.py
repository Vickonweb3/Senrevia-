"""Alerts menu handlers."""

from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from bot.keyboards.menus import back_main
from database import repositories as repo


async def show_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    query = update.callback_query
    message = update.effective_message
    if not user:
        return
    doc = repo.get_user(user.id) or {}
    settings = doc.get("settings") or {}
    enabled = settings.get("alerts_enabled", True)
    status = "enabled" if enabled else "paused"
    text = (
        "🔔 *Alerts*\n"
        "\n"
        f"Notifications are currently *{status}*.\n"
        "\n"
        "When alerts are on, Senrivia notifies you about:\n"
        "• New replies left by accounts you watch\n"
        "• New follows detected after the baseline\n"
        "\n"
        "Manage delivery from *Settings*."
    )
    if query:
        await query.answer()
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_main())
    elif message:
        await message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_main())


def register(app: Application) -> None:
    app.add_handler(CommandHandler("alerts", show_alerts))
    app.add_handler(CallbackQueryHandler(show_alerts, pattern=r"^menu:alerts$"))
