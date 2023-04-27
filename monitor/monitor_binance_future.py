import ccxt.async_support as ccxt_async
import asyncio
import os

api_key = 'your_api_key'
api_secret = 'your_api_secret'

exchange = ccxt_async.binance({
    # 'apiKey': api_key,
    # 'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    },
})

async def print_future_price(symbol):
    while True:
        try:
            ticker = await exchange.fetch_ticker(symbol)
            print(f"{symbol} price: {ticker['last']}")
            await asyncio.sleep(5)  # Adjust the sleep interval as needed
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(60)

symbol = 'BTC/USDT'

loop = asyncio.get_event_loop()
loop.run_until_complete(print_future_price(symbol))


