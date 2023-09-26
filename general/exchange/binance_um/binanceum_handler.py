from general.exchange.type_enum import BINANCEUM
from general.exchange.exchange_handler import ExchangeHandler
from binance.um_futures import UMFutures
from general.exchange.type_enum import (
    BUY, SELL, MARKET, LIMIT,
    GTC, IOC, FOK, POST_ONLY
)


class BinanceUMHandler(ExchangeHandler):
    NAME = BINANCEUM

    def __init__(self, api_key='', api_secret=''):
        self.um_futures = UMFutures(key=api_key, secret=api_secret)

    def create_market_order(self, symbol, side, qty):
        ret = self.um_futures.new_order(symbol=symbol, side=side, type=MARKET, quantity=qty)
        return ret

    def create_limit_order(self, symbol, side, qty, price, time_in_force=GTC):
        ret = self.um_futures.new_order(symbol=symbol, side=side, type=LIMIT, quantity=qty, price=price,
                                        timeInForce=time_in_force)
        return ret

    @staticmethod
    def to_market_price(data):
        return {
            '_id': data['E'],
            'ex': BinanceUMHandler.NAME,
            'b': data['b'][0][0],
            'a': data['a'][0][0],
            't': data['T']
        }


