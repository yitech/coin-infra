from typing import Dict


class ExchangeHandler:

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
