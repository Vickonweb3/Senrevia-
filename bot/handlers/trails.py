"""Trail view handlers."""

from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from bot.keyboards.menus import back_main
from database import repositories as repo
from services.trail import format_trail_lines


async def show_trails_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not update.message:
        return
    events = repo.list_trails_for_user(user.id, limit=15)
    body = format_trail_lines(events)
    text = f"🧵 *Your Trails*\n\n{body}"
    await update.message.reply_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_main(), disable_web_page_preview=True
    )


async def show_trails(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.effective_user
    if not query or not user:
        return
    await query.answer()
    events = repo.list_trails_for_user(user.id, limit=15)
    body = format_trail_lines(events)
    await query.edit_message_text(
        f"🧵 *Your Trails*\n\n{body}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_main(),
        disable_web_page_preview=True,
    )


async def trail_for_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    handle = query.data.split(":", 1)[1]
    await query.answer()
    events = repo.list_trails_for_handle(handle, limit=15)
    filtered = [
        e
        for e in events
        if e.get("kind") == "reply" or (e.get("kind") == "follow" and e.get("is_new"))
    ]
    if not filtered:
        filtered = [e for e in events if e.get("kind") == "reply"]
    body = format_trail_lines(filtered or events)
    await query.edit_message_text(
        f"🧵 *Trail — @{handle}*\n\n{body}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_main(),
        disable_web_page_preview=True,
    )


def register(app: Application) -> None:
    app.add_handler(CommandHandler("trails", show_trails_message))
    app.add_handler(CallbackQueryHandler(show_trails, pattern=r"^menu:trails$"))
    app.add_handler(CallbackQueryHandler(trail_for_handle, pattern=r"^trail:"))
