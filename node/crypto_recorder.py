import ccxt.async_support as ccxt_async
import asyncio


class BinanceFutureRPC:
    def __init__(self, name: str, exchange_id: str, api_key: str, api_secret: str, kafka_server: str):
        self.name: str = name

        self.exchange = ccxt_async.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
            },
        })

        self.kafka_server: str = kafka_server
        self.producer = P

    async def fetch_ticket(self, symbol, target):
        ticker = await self.exchange.fetch_ticker(symbol)


    def run(self, exchange_id: str, symbol: str, period: float, depth: int):
        # Initialize the exchange
        exchange = getattr(ccxt, exchange_id)()

        # Load markets
        exchange.load_markets()

        # Fetch order book
        order_book = exchange.fetch_order_book(symbol)

        # Return the order book
        return order_book





