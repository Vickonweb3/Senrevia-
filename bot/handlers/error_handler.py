"""Error handlers."""
# Handles errors and exceptions in the bot

async def error_handler(update, context):
    """Handle errors in the bot."""
    logger = logging.getLogger(__name__)
    logger.error(f'Update {update} caused error {context.error}')
