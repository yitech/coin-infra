import unittest
from general.exchange.okx import OKXHandler


class TestOKXHandler(unittest.TestCase):
    def setUp(self):
        self.okx_handler = OKXHandler(api_key='3bf7276d-1b16-4566-98f1-5f02498faccd',
                                      api_secret='7F346D60A6D0F9E337A21D0BAEC0254E',
                                      passphrase='colw2q8+aU')

    def test_create_market_order(self):
        res = self.okx_handler.create_market_order('LTC','USDT', 'buy', 1.0, dry_run=True)
        self.assertTrue(res["data"])

    def test_create_limit_order(self):
        res = self.okx_handler.create_limit_order('LTC','USDT', 'buy', 1.0, 55, dry_run=True)
        self.assertTrue(res["data"])

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


if __name__ == '__main__':
    unittest.main()