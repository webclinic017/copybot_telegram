"""
Trading bot based on Telegram indicators
"""

import asyncio
import os
import re

from dotenv import load_dotenv
from telethon import TelegramClient

from position import ActionType, Position


async def main():
    """Main function"""

    # load .env variables
    load_dotenv()

    # create a client
    client = TelegramClient(
        "session_name", os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH")
    )

    # start the client
    await client.start()

    # get the group
    group = await client.get_entity(os.getenv("TELEGRAM_CHAT"))

    # get the messages
    async for message in client.iter_messages(group, limit=50):

        # get time and text
        time = message.date
        text = message.message.lower().replace("ß", "ss")

        # close a position
        if "ich schliesse" in text:
            try:
                symbol = re.search(r"ich schliesse (.*?)\u2757", text).group(1)
                position = Position(time=time, symbol=symbol, action=ActionType.CLOSE)
                print(position.to_csv())
            except Exception as error:  # pylint: disable=broad-except
                print("Skipping CLOSE position. Error: ", error)

        # open a position
        if "live trend" in text:

            if "ich kaufe" in text:
                try:
                    symbol = re.search(r"ich kaufe (.*?) ", text).group(1)
                    position = Position(time=time, symbol=symbol, action=ActionType.BUY)
                    print(position.to_csv())
                except Exception as error:  # pylint: disable=broad-except
                    print("Skipping BUY position. Error: ", error)

            if "ich verkaufe" in text:
                try:
                    symbol = re.search(r"ich verkaufe (.*?) ", text).group(1)
                    position = Position(
                        time=time, symbol=symbol, action=ActionType.SELL
                    )
                    print(position.to_csv())
                except Exception as error:  # pylint: disable=broad-except
                    print("Skipping SELL position. Error: ", error)


if "__main__" == __name__:
    asyncio.run(main())
