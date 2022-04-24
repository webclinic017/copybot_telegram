"""TradingSignal Class"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradingSignal:
    """Signals used to buy or sell currencies."""

    time: datetime = datetime.now()
    symbol: str = None
    action: str = None

    def to_csv(self):
        """Convert to csv"""

        return f"{self.time},{self.symbol},{self.action}"
