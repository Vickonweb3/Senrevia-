# Telegram Custom Emoji ID Extractor

Standalone Telethon utility for reading Telegram `MessageEntityCustomEmoji` document IDs.

## Setup

1. Create Telegram API credentials at https://my.telegram.org.
2. Copy `.env.example` to `.env` and fill in `API_ID` and `API_HASH`.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python emoji_extractor.py`
5. Complete the Telegram login once. A local session file will be created.
6. Forward/send a custom emoji to **Saved Messages**.

The tool prints the custom emoji `document_id`. It does not use or modify the Senrivia bot.
