"""
Trading bot based on Telegram indicators
"""

import asyncio
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from telethon import TelegramClient

from position import Position, PositionType


async def main():
    """Main function"""

    # load variables
    load_dotenv()
    TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
    TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
    TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT")

    # create a client
    client = TelegramClient("session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)

    # start the client
    await client.start()

    # get the group
    group = await client.get_entity(TELEGRAM_CHAT)

    # get the messages
    async for message in client.iter_messages(group, limit=1):

        # get datetime and text
        text = message.message.lower().replace("ß", "ss")
        time = message.date
        now = datetime.now(tz=time.tzinfo)
        delay = (now - time).seconds

        print(text)

        # check if the message is a trade
        if "live trend" in text:

            if "ich kaufe" in text:
                try:
                    symbol = re.search(r"ich kaufe (.*?) ", text).group(1)
                    open_price = float(re.search(r"\(ek: (.*)\)", text).group(1))

                    position = Position(
                        time=time,
                        delay=delay,
                        symbol=symbol,
                        type=PositionType.BUY,
                        open_price=open_price,
                    )

                    print(position)
                except Exception as error:  # pylint: disable=broad-except
                    print("Skipping position. Error: ", error)


if "__main__" == __name__:
    asyncio.run(main())
