"""Bot based on Telegram live trading signals."""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from telethon import TelegramClient, events

from exchange.libertex import Libertex
from trading_signal import TradingSignal

# load .env variables
load_dotenv()

# initialize exchange
libertex = Libertex()

# create a client
client = TelegramClient(
    "session_name", os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH")
)


@client.on(events.NewMessage(chats=["Test", os.getenv("TELEGRAM_CHAT")]))
async def process(event):
    """Process new messages."""

    # get time and text
    time = event.date
    text = event.message.message.lower().replace("ß", "ss")

    signal = TradingSignal(time, text)
    if signal.is_valid:
        print(signal.to_csv())
        await client.send_message("Test", signal.to_csv())

        # Execute on Libertex
        if signal.action == "BUY":
            response = libertex.open_position(signal.symbol, "BUY")
        elif signal.action == "SELL":
            response = libertex.open_position(signal.symbol, "SELL")
        elif signal.action == "CLOSE":
            response = libertex.close_positions(signal.symbol)
        elif signal.action.startswith("SL="):
            response = libertex.set_stop_loss(
                signal.symbol, signal.action.split("=")[1]
            )
        else:
            response = "Signal not configured"

        print(response)
        await client.send_message("Test", str(response))


if "__main__" == __name__:

    now = (
        datetime.utcnow()
        .replace(tzinfo=timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )
    print(f"{now} Listening on new Telegram messages...")

    client.start()
    client.run_until_disconnected()
