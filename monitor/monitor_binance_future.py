import argparse
import json
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


async def main(symbol, delay, output_format, depth):
    while True:
        try:
            ticker = await exchange.fetch_ticker(symbol)
            orderbook = await exchange.fetch_order_book(symbol, limit=depth)
            bids = orderbook['bids']
            asks = orderbook['asks']

            if output_format == 'text':
                print(f"{symbol} price: {ticker['last']}")
                print("Bids:")
                for bid in bids:
                    print(f"  Price: {bid[0]}, Amount: {bid[1]}")
                print("Asks:")
                for ask in asks:
                    print(f"  Price: {ask[0]}, Amount: {ask[1]}")
            elif output_format == 'json':
                data = {
                    'symbol': symbol,
                    'price': ticker['last'],
                    'bids': bids,
                    'asks': asks,
                }
                print(json.dumps(data))

            await asyncio.sleep(delay)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)
        finally:
            await exchange.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor the spot price of a trading pair on Binance.")
    parser.add_argument("symbol", help="Trading pair symbol (e.g., BTC/USDT).")
    parser.add_argument("delay", type=float, help="Time delay between price fetches in seconds.")
    parser.add_argument("--format", choices=['text', 'json'], default='text', help="Output format: text or json.")
    parser.add_argument("--depth", type=int, default=5, help="Number of levels to fetch from the order book.")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.symbol, args.delay, args.format, args.depth))


