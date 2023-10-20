from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Orderbook:
    timestamp: int
    ask: List[Tuple[float, float]]
    bid: List[Tuple[float, float]]

