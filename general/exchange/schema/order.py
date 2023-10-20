from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    status: str
    updated_time: int
    base: str
    quote: str
    qty: float
    side: str
    filled: float
    price: float
