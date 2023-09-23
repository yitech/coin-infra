from general.exchange.type_enum import BINANCEUM, OKX
from general.exchange.binance_um import BinanceUMHandler
from general.exchange.okx import OKXHandler


class ExchangeFactory:
    @staticmethod
    def get_handler(exchange: str, *api):
        if exchange == BINANCEUM:
            return BinanceUMHandler(api[0], api[1])
        elif exchange == OKX:
            return OKXHandler(api[0], api[1])
        else:
            raise ValueError(f"{exchange} not implemented yet")

