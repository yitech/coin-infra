import logging
from general.exchange.type_enum import BINANCEUM
from general.exchange.exchange_handler import ExchangeHandler
from binance.um_futures import UMFutures
from binance.error import ClientError
from general.exchange.type_enum import (
    BUY, SELL, MARKET, LIMIT,
    GTC, IOC, FOK, POST_ONLY
)


class BinanceUMHandler(ExchangeHandler):
    NAME = BINANCEUM

    def __init__(self, api_key='', api_secret='', logger=None):
        super().__init__(logger)
        self.um_futures = UMFutures(key=api_key, secret=api_secret)

    def create_market_order(self, symbol, side, qty):
        try:
            ret = self.um_futures.new_order(symbol=symbol, side=side, type=MARKET, quantity=qty)
            return ret
        except ClientError as error:
            self.logger.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def create_limit_order(self, symbol, side, qty, price, time_in_force=GTC):
        try:
            ret = self.um_futures.new_order(symbol=symbol, side=side, type=LIMIT, quantity=qty, price=price,
                                            timeInForce=time_in_force)
            return ret
        except ClientError as error:
            self.logger.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    @staticmethod
    def to_market_price(data):
        return {
            '_id': data['E'],
            'ex': BinanceUMHandler.NAME,
            'b': data['b'][0][0],
            'a': data['a'][0][0],
            't': data['T']
        }


