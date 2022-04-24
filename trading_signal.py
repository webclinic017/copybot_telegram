"""TradingSignal Class"""

import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradingSignal:
    """Signals used to buy or sell currencies."""

    time: datetime = datetime.now()
    symbol: str = None
    action: str = None
    is_valid: bool = False

    def to_csv(self):
        """Convert to csv"""

        return f"{self.time},{self.symbol},{self.action}"

    def __init__(self, time, text):
        """Parse signal from Telegram chat."""

        self.time = time

        # open a position
        if "live trend" in text:

            if "ich kaufe" in text:
                try:
                    self.symbol = re.search(r"ich kaufe (.*?) ", text).group(1)
                    self.action = "BUY"
                    self.is_valid = True
                except Exception as error:  # pylint: disable=broad-except
                    print("Skipping BUY signal. Error: ", error)

            if "ich verkaufe" in text:
                try:
                    self.symbol = re.search(r"ich verkaufe (.*?) ", text).group(1)
                    self.action = "SELL"
                    self.is_valid = True
                except Exception as error:  # pylint: disable=broad-except
                    print("Skipping SELL signal. Error: ", error)

        # close a position
        if "ich schliesse" in text:
            try:
                self.symbol = re.search(r"ich schliesse (.*?)\u2757", text).group(1)
                self.action = "CLOSE"
                self.is_valid = True
            except Exception as error:  # pylint: disable=broad-except
                print("Skipping CLOSE signal. Error: ", error)

        # set stop loss
        if "sl:" in text:
            try:
                self.symbol = re.search(r"(.*?) sl:", text).group(1)
                stop_loss = float(re.search(r"sl:(.*)", text).group(1))
                self.action = f"SL={stop_loss}"
                self.is_valid = True
            except Exception as error:  # pylint: disable=broad-except
                print("Skipping SL signal. Error: ", error)
