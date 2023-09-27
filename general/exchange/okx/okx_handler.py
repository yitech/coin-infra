import traceback
import ccxt
from general.exchange.type_enum import OKX
from general.exchange.exchange_handler import ExchangeHandler
from general.exchange.type_enum import (
    GTC
)


class OKXHandler(ExchangeHandler):
    NAME = OKX

    def __init__(self, api_key='', api_secret='', passphrase='', logger=None):
        super().__init__(logger)
        self.okx = ccxt.okex5(
            {
                'apiKey': api_key,
                'secret': api_secret,
                'password': passphrase,
                'options': {
                    'defaultType': 'swap'
                },
            }
        )

    def create_market_order(self, symbol, side, qty):
        try:
            res = self.okx.create_order(symbol, 'market', side.lower(), qty)
            return res
        except ccxt.BaseError as e:
            self.logger.error(f"Missing key in message: {e}\n{traceback.format_exc()}")

    def create_limit_order(self, symbol, side, qty, price, time_in_force=GTC):
        try:
            res = self.okx.create_order(symbol, 'limit', side.lower(), qty, price)
            return res
        except ccxt.BaseError as e:
            self.logger.error(f"Missing key in message: {e}\n{traceback.format_exc()}")

    @staticmethod
    def to_market_price(data):
        data = data['data'][0]
        return {
            '_id': data['seqId'],
            'ex': OKXHandler.NAME,
            'b': data['bids'][0][0],    
            'a': data['asks'][0][0],
            't': int(data['ts'])
        }
