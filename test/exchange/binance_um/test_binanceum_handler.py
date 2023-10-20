import time
import unittest
import logging
from general.exchange.binance_um import BinanceUMHandler


class TestBinanceUMHandler(unittest.TestCase):
    def setUp(self):
        self.binance_handler = BinanceUMHandler(api_key='4ir7rcqDpj85F4jMq9YqBYssJs8kmdMQuuE1wAG2yLFTpQ6auqax0CgiHR9bcpfC',
                                                api_secret='TwnuVpetM5mRfpL7XqSQzcakFGjOKzAPyYBBkuskITq8jP9jof3x7fuNMlGHVm2v')
        logging.basicConfig(level=logging.INFO)

    def test_create_market_order(self):
        ret = self.binance_handler.create_market_order('LTC', 'USDT', 'BUY', 1, dry_run=False)
        logging.info(f"{ret=}")

    def test_create_limit_order(self):
        ret = self.binance_handler.create_limit_order('LTC', 'USDT', 'BUY', 1, 50, dry_run=True)
        logging.info(f"{ret=}")

    def test_get_orderbook(self):
        ret = self.binance_handler.get_orderbook('LTC', 'USDT')
        logging.info(f"{ret=}")

    def test_cancel_all_order(self):
        ret = self.binance_handler.create_limit_order('LTC', 'USDT', 'BUY', 1, 50, dry_run=False)
        self.assertTrue(ret['status'], 'NEW')
        time.sleep(3)
        ret = self.binance_handler.cancel_all_order('LTC', 'USDT')
        self.assertTrue(ret['code'], 200)

    def test_get_open_order(self):
        self.binance_handler.cancel_all_order('LTC', 'USDT')
        ret = self.binance_handler.create_limit_order('LTC', 'USDT', 'BUY', 1, 55, dry_run=False)
        logging.info(f"{ret=}")
        time.sleep(1)
        ret = self.binance_handler.get_open_order('LTC', 'USDT')
        logging.info(f"{ret=}")
        self.binance_handler.cancel_all_order('LTC', 'USDT')

    def test_get_account_trade(self):
        ret = self.binance_handler.get_account_trades('LTC', 'USDT')
        logging.info(f"{ret=}")

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