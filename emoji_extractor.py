import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient, events, types

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.getenv("SESSION", "custom_emoji_session")

client = TelegramClient(SESSION, API_ID, API_HASH)


def inspect_message(message):
    found = []
    for entity in message.entities or []:
        if isinstance(entity, types.MessageEntityCustomEmoji):
            if entity.document_id not in found:
                found.append(entity.document_id)
    return found


async def main():
    print("Telegram Custom Emoji ID Extractor")
    print("Send/forward a custom emoji to Saved Messages.")
    print("The extractor prints the Telegram custom emoji document ID.\n")

    await client.start()
    me = await client.get_me()
    print(f"Logged in as: {getattr(me, 'username', None) or me.first_name}")
    print("Waiting for messages... Press Ctrl+C to stop.\n")

    @client.on(events.NewMessage(chats="me"))
    async def handler(event):
        ids = inspect_message(event.message)
        if not ids:
            print("No Telegram custom emoji entity found in that message.")
            return
        print("Custom emoji ID(s):")
        for document_id in ids:
            print(document_id)
        print()

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
