"""Bot based on Telegram history trading signals."""

import asyncio
import collections
import os
import sys

from dotenv import load_dotenv
from telethon import TelegramClient

from trading_signal import TradingSignal

# Set the policy to prevent "Event loop is closed" error on Windows
# https://github.com/encode/httpx/issues/914
if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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
    symbols = []
    async for message in client.iter_messages(group, limit=50):

        # get time and text
        time = message.date
        text = message.message.lower().replace("ß", "ss")

        signal = TradingSignal(time, text)
        if signal.is_valid:
            print(signal.to_csv())

            # add traded symbol to list
            symbols.append(signal.symbol)

    counter = collections.Counter(symbols)
    print("Symbols/frequency: " + str(counter))


if "__main__" == __name__:
    asyncio.run(main())
