import ccxt.async_support as ccxt_async


class BinanceFuture:
    def __init__(self, name: str, api_key: str, api_secret: str):
        self.name: str = name

        self.exchange = ccxt_async.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
            },
        })

    async def fetch_ticker(self, symbol):
        ticker = await self.exchange.fetch_ticker(symbol)
        return ticker

    async def fetch_order_book(self, symbol):
        orderbook = await self.exchange.fetch_order_book(symbol)
        return orderbook





