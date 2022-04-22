"""PositionClass"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PositionType(Enum):
    """Enum for position type"""

    BUY = 1
    SELL = -1


@dataclass
class Position:
    """Position class"""

    time: datetime = datetime.now()
    delay: int = 0
    symbol: str = None
    type: PositionType = None
    open_price: float = None
    close_price: float = None
    is_closed: bool = False
    profit: float = 0
