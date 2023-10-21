import time
import unittest
import logging
from general.exchange.okx import OKXHandler


class TestOKXHandler(unittest.TestCase):
    def setUp(self):
        self.okx_handler = OKXHandler(api_key='3bf7276d-1b16-4566-98f1-5f02498faccd',
                                      api_secret='7F346D60A6D0F9E337A21D0BAEC0254E',
                                      passphrase='colw2q8+aU')
        logging.basicConfig(level=logging.INFO)

    def test_create_market_order(self):
        ret = self.okx_handler.create_market_order('LTC','USDT', 'buy', 1.0, dry_run=False)
        logging.info(f"{ret=}")
        # self.assertTrue(res["data"])

    def test_create_limit_order(self):
        ret = self.okx_handler.create_limit_order('LTC','USDT', 'buy', 1.0, 55, dry_run=False)
        logging.info(f"{ret=}")
        self.assertTrue(ret["data"])

    def test_cancel_all_order(self):
        ret = self.okx_handler.create_limit_order('LTC', 'USDT', 'buy', 1.0, 55, dry_run=False)
        logging.info(f"{ret=}")
        time.sleep(1)
        ret = self.okx_handler.cancel_all_order('LTC', 'USDT')
        logging.info(f"{ret=}")

    def test_get_open_order(self):
        ret = self.okx_handler.get_open_order('LTC', 'USDT')
        logging.info(f"{ret=}")

    def test_get_orderbook(self):
        ret = self.okx_handler.get_orderbook('LTC', 'USDT')
        logging.info(f"{ret=}")

    def test_get_account_trades(self):
        ret = self.okx_handler.get_account_trades('LTC', 'USDT')
        logging.info(f"{ret=}")

    def test_to_market_price(self):
        data = {'data': [{'seqId': '123', 'bids': [[50000.0, 1]], 'asks': [[50001.0, 1]], 'ts': 1633027200000}]}
        res = OKXHandler.to_market_price(data)
        expected = {
            '_id': '123',
            'ex': 'OKX',
            'b': 50000.0,
            'a': 50001.0,
            't': 1633027200000
        }
        self.assertEqual(res, expected)

    def test_to_orderbook(self):
        data = {"data": [
            {"asks": [["64.73", "536", "0", "13"], ["64.74", "956", "0", "18"]],
             "bids": [["64.72", "48", "0", "1"], ["64.71", "872", "0", "16"]],
             "instId": "LTC-USDT-SWAP", "ts": "1697896467806"}]}
        res = OKXHandler.to_orderbook(data)
        expected = {
            'exchange': 'OKX',
            'timestamp': '1697896467806',
            'ask': [(64.73, 536.0), (64.74, 956.0)],
            'bid': [(64.72, 48.0), (64.71, 872.0)]
        }


if __name__ == '__main__':
    unittest.main()