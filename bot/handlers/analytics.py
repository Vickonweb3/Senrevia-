"""Analytics handlers."""

from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from bot.keyboards.menus import back_main
from services.analytics import user_analytics


def _text(stats: dict) -> str:
    return (
        "📊 *Senrivia Analytics*\n"
        "\n"
        f"Tracked: *{stats['tracked']}*\n"
        f"Active: *{stats['active']}*\n"
        f"Paused: *{stats['paused']}*\n"
        "\n"
        f"Mapped replies: *{stats['replies']}*\n"
        f"New follows detected: *{stats['new_follows']}*\n"
        "\n"
        "_Figures reflect your personal watchlist._"
    )


async def show_analytics_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not update.message:
        return
    stats = user_analytics(user.id)
    await update.message.reply_text(
        _text(stats), parse_mode=ParseMode.MARKDOWN, reply_markup=back_main()
    )


async def show_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.effective_user
    if not query or not user:
        return
    await query.answer()
    stats = user_analytics(user.id)
    await query.edit_message_text(
        _text(stats), parse_mode=ParseMode.MARKDOWN, reply_markup=back_main()
    )


def register(app: Application) -> None:
    app.add_handler(CommandHandler("analytics", show_analytics_message))
    app.add_handler(CallbackQueryHandler(show_analytics, pattern=r"^menu:analytics$"))
