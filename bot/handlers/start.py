"""Start command handler."""

from bot.services.users import get_user_registry


async def start_handler(update, context):
    """Register the user so admins can broadcast to them."""
    if update.effective_user and update.effective_chat:
        get_user_registry().register(update.effective_user, update.effective_chat.id)

    await update.effective_message.reply_text(
        "Welcome to Senrivia! Your account has been registered."
    )
