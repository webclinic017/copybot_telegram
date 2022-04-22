"""PositionClass"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ActionType(Enum):
    """Enum for action type"""

    BUY = 1
    SELL = -1
    CLOSE = 0


@dataclass
class Position:
    """Position class"""

    time: datetime = datetime.now()
    symbol: str = None
    action: ActionType = None
    stop_loss: float = None

    def to_csv(self):
        """Convert to csv"""

        return f"{self.time},{self.symbol},{self.action.value},{self.stop_loss}"
