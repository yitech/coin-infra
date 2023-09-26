import logging
from typing import Dict


class ExchangeHandler:
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = logging.Logger(ExchangeHandler.__name__)

    @staticmethod
    def to_market_price(data: Dict) -> Dict:
        """
        Convert exchange orderbook data to schema
        {
            _id: int,
            ex: str,
            a: float
            b: float
            t: int
        }
        """
        return data
