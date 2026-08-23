"""Search influencer handlers."""

from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

from bot.keyboards.menus import back_main, influencer_actions
from database import repositories as repo
from scraper import clean_handle
from services.influencer import format_followers, search_influencer, watch_influencer


SEARCH_PROMPT = (
    "🔎 *Search Influencer*\n"
    "\n"
    "Send a public X username to inspect.\n"
    "Example: `@NASA` or `NatGeo`"
)


async def prompt_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["awaiting_search"] = True
    text = SEARCH_PROMPT
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_main()
        )
    elif update.message:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_main()
        )


async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        await run_search(update, context, " ".join(context.args))
        return
    await prompt_search(update, context)


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get("awaiting_search"):
        return
    if not update.message or not update.message.text:
        return
    if update.message.text.startswith(("🔎", "👤", "🧵", "📊", "⚙️")):
        return
    context.user_data["awaiting_search"] = False
    await run_search(update, context, update.message.text)


async def run_search(update: Update, context: ContextTypes.DEFAULT_TYPE, raw: str) -> None:
    user = update.effective_user
    message = update.effective_message
    if not user or not message:
        return
    repo.upsert_user(
        user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
    )
    handle = clean_handle(raw)
    if not handle:
        await message.reply_text(
            "That username does not look valid. Try again with letters, numbers, or underscores.",
            reply_markup=back_main(),
        )
        context.user_data["awaiting_search"] = True
        return
    status = await message.reply_text(f"Looking up @{handle}…")
    try:
        profile = await search_influencer(handle)
    except LookupError:
        await status.edit_text(
            f"Could not find **@{handle}**.\nCheck the spelling and try again.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_main(),
        )
        return
    except Exception as exc:
        await status.edit_text(f"Lookup failed: {exc}", reply_markup=back_main())
        return

    watching = any(
        w.get("handle_lower") == profile["handle"].lower()
        for w in repo.list_watchlist(user.id)
    )
    followers = format_followers(profile.get("followers_count"))
    bio = (profile.get("bio") or "—").replace("\n", " ")
    if len(bio) > 180:
        bio = bio[:177] + "…"
    verified = " ✓" if profile.get("verified") else ""
    text = (
        f"👤 *@{profile['handle']}*{verified}\n"
        f"{profile.get('display_name') or profile['handle']}\n"
        f"\n"
        f"Followers: *{followers}*\n"
        f"Bio: _{bio}_\n"
        f"\n"
        f"{'You are already watching this account.' if watching else 'Not on your watchlist yet.'}"
    )
    await status.edit_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=influencer_actions(profile["handle"], watching=watching),
        disable_web_page_preview=True,
    )


async def on_watch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    handle = query.data.split(":", 1)[1]
    user = update.effective_user
    if not user:
        return
    await query.answer("Adding to watchlist…")
    try:
        result = await watch_influencer(user.id, handle)
        profile = result["profile"]
        await query.edit_message_text(
            (
                f"✅ Now watching *@{profile['handle']}*\n"
                f"\n"
                f"Senrivia will map replies and new follows for this account.\n"
                f"You can pause tracking any time from *My Influencers*."
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=influencer_actions(profile["handle"], watching=True),
        )
    except Exception as exc:
        await query.edit_message_text(
            f"Could not start watching @{handle}: {exc}",
            reply_markup=back_main(),
        )


def register(app: Application) -> None:
    app.add_handler(CommandHandler("search", cmd_search))
    app.add_handler(CallbackQueryHandler(prompt_search, pattern=r"^menu:search$"))
    app.add_handler(CallbackQueryHandler(on_watch, pattern=r"^watch:"))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_text),
        group=1,
    )
