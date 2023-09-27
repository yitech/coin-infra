import unittest
from unittest.mock import patch
from general.exchange.binance_um import BinanceUMHandler


class TestBinanceUMHandler(unittest.TestCase):
    def setUp(self):
        self.binance_handler = BinanceUMHandler(api_key='4ir7rcqDpj85F4jMq9YqBYssJs8kmdMQuuE1wAG2yLFTpQ6auqax0CgiHR9bcpfC',
                                                api_secret='TwnuVpetM5mRfpL7XqSQzcakFGjOKzAPyYBBkuskITq8jP9jof3x7fuNMlGHVm2v')

    def test_create_market_order(self):
        ret = self.binance_handler.create_market_order('LTCUSDT', 'BUY', 1, dry_run=True)
        self.assertEqual(ret['orderId'], 0)

    def test_create_limit_order(self):
        ret = self.binance_handler.create_limit_order('LTCUSDT', 'BUY', 1, 50, dry_run=True)
        self.assertEqual(ret['orderId'], 0)

    def test_to_market_price(self):
        data = {
            'E': 'test_id',
            'b': [['price_b', 'volume_b']],
            'a': [['price_a', 'volume_a']],
            'T': 'test_time'
        }
        expected = {
            '_id': 'test_id',
            'ex': 'BinanceUM',
            'b': 'price_b',
            'a': 'price_a',
            't': 'test_time'
        }
        self.assertEqual(BinanceUMHandler.to_market_price(data), expected)

if __name__ == '__main__':
    unittest.main()