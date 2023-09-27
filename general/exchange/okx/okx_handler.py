import traceback
from okex.Trade_api import TradeAPI
from general.exchange.type_enum import OKX
from general.exchange.exchange_handler import ExchangeHandler
from general.exchange.type_enum import (
    GTC
)


class OKXHandler(ExchangeHandler):
    NAME = OKX

    def __init__(self, api_key='', api_secret='', passphrase='', logger=None):
        super().__init__(logger)
        self.okx_trade = TradeAPI(api_key, api_secret, passphrase)

    def create_market_order(self, symbol, side, qty, dry_run=False):
        try:
            if dry_run:
                res = {'orderId': 0}
            else:
                res = self.okx_trade.place_order(symbol, 'cross', side, 'market', qty)
            return res
        except Exception as e:
            self.logger.error(f"Missing key in message: {e}\n{traceback.format_exc()}")

    def create_limit_order(self, symbol, side, qty, price, time_in_force=GTC, dry_run=False):
        try:
            if dry_run:
                res = {'orderId': 0}
            else:
                res = self.okx_trade.place_order(symbol, 'cross', side, 'limit', qty, px=price)
            return res
        except Exception as e:
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
