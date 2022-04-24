"""Bot based on Telegram history trading signals."""

import asyncio
import os
import re
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
    async for message in client.iter_messages(group, limit=50):

        # get time and text
        time = message.date
        text = message.message.lower().replace("ß", "ss")

        # open a position
        if "live trend" in text:

            if "ich kaufe" in text:
                try:
                    symbol = re.search(r"ich kaufe (.*?) ", text).group(1)
                    signal = TradingSignal(time=time, symbol=symbol, action="BUY")
                    print(signal.to_csv())
                except Exception as error:  # pylint: disable=broad-except
                    print("Skipping BUY signal. Error: ", error)

            if "ich verkaufe" in text:
                try:
                    symbol = re.search(r"ich verkaufe (.*?) ", text).group(1)
                    signal = TradingSignal(time=time, symbol=symbol, action="SELL")
                    print(signal.to_csv())
                except Exception as error:  # pylint: disable=broad-except
                    print("Skipping SELL signal. Error: ", error)

        # close a position
        if "ich schliesse" in text:
            try:
                symbol = re.search(r"ich schliesse (.*?)\u2757", text).group(1)
                signal = TradingSignal(time=time, symbol=symbol, action="CLOSE")
                print(signal.to_csv())
            except Exception as error:  # pylint: disable=broad-except
                print("Skipping CLOSE signal. Error: ", error)

        # set stop loss
        if "sl:" in text:
            try:
                symbol = re.search(r"(.*?) sl:", text).group(1)
                stop_loss = float(re.search(r"sl:(.*)", text).group(1))
                signal = TradingSignal(
                    time=time, symbol=symbol, action=f"SL={stop_loss}"
                )
                print(signal.to_csv())
            except Exception as error:  # pylint: disable=broad-except
                print("Skipping SL signal. Error: ", error)


if "__main__" == __name__:
    asyncio.run(main())
