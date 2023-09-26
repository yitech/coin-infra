from general.exchange.type_enum import OKX
from general.exchange.exchange_handler import ExchangeHandler
import ccxt


class OKXHandler(ExchangeHandler):
    NAME = OKX

    def __init__(self, api_key='', api_secret='', passphrase=''):
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

    @staticmethod
    def to_market_price(data):
        return {
            '_id': data['seqId'],
            'ex': OKXHandler.NAME,
            'b': data['bids'][0][0],
            'a': data['asks'][0][0],
            't': int(data['ts'])
        }

