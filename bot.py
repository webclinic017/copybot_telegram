"""Bot based on Telegram live trading signals."""

import os
from datetime import datetime

from dotenv import load_dotenv
from telethon import TelegramClient, events

# load .env variables
load_dotenv()

# create a client
client = TelegramClient(
    "session_name", os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH")
)


@client.on(events.NewMessage(chats=["Test", os.getenv("TELEGRAM_CHAT")]))
async def process(event):
    """Process new messages."""

    # get time and text
    time = event.date
    text = event.message.message

    print(time, text)

    await client.send_message("Test", text)


if "__main__" == __name__:

    print(f"{datetime.now()} Listening on new Telegram messages...")

    client.start()
    client.run_until_disconnected()
