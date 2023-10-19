from general.exchange.type_enum import BINANCEUM
from general.exchange.exchange_handler import ExchangeHandler
from binance.um_futures import UMFutures
from binance.error import ClientError
from general.exchange.type_enum import (
    MARKET, LIMIT,
    GTC
)
from .utils import to_side, to_symbol


def handle_client_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientError as error:
            # Assuming the first argument to the function is `self`
            args[0].logger.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
    return wrapper


class BinanceUMHandler(ExchangeHandler):
    NAME = BINANCEUM

    def __init__(self, api_key='', api_secret='', logger=None):
        super().__init__(logger)
        self.um_futures = UMFutures(key=api_key, secret=api_secret)

    @handle_client_error
    def create_market_order(self, base, quote, side, qty, dry_run=False):
        if dry_run:
            ret = self.um_futures.new_order_test(symbol=to_symbol(base, quote), side=to_side(side), type=MARKET,
                                                 quantity=qty)
        else:
            ret = self.um_futures.new_order(symbol=to_symbol(base, quote), side=to_side(side), type=MARKET,
                                            quantity=qty)
        return ret

    @handle_client_error
    def create_limit_order(self, base, quote, side, qty, price, time_in_force=GTC, dry_run=False):
        if dry_run:
            ret = self.um_futures.new_order_test(symbol=to_symbol(base, quote), side=to_side(side), type=LIMIT, quantity=qty, price=price,
                                                 timeInForce=time_in_force)
        else:
            ret = self.um_futures.new_order(symbol=to_symbol(base, quote), side=to_side(side), type=LIMIT, quantity=qty, price=price,
                                            timeInForce=time_in_force)
        return ret

    @handle_client_error
    def cancel_all_order(self, base, quote):
        ret = self.um_futures.cancel_open_orders(symbol=to_symbol(base, quote))
        return ret

    @handle_client_error
    def get_orderbook(self, base, quote):
        ret = self.um_futures.depth(symbol=to_symbol(base, quote))
        return ret

    @handle_client_error
    def get_open_order(self, base, quote):
        ret = self.um_futures.get_all_orders(symbol=to_symbol(base, quote))
        print(f"{ret=}")
        ret = list(filter(lambda order: order["status"] == 'NEW', ret))
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
