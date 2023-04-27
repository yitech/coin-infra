import argparse
import asyncio
import ccxt.async_support as ccxt_async
import json
import os

api_key = '5b26a0c1-cf08-4815-af1c-bb8a4688678a'
api_secret = 'ED7C623550788523A14CE060CDAD40FD'

exchange = ccxt_async.okx({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
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
                print(json.dumps(data, indent=2))

            await asyncio.sleep(delay)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)
        finally:
            await exchange.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor the spot price of a trading pair on OKX.")
    parser.add_argument("symbol", help="Trading pair symbol (e.g., BTC/USDT).")
    parser.add_argument("delay", type=int, help="Time delay between price fetches in seconds.")
    parser.add_argument("--format", choices=['text', 'json'], default='text', help="Output format: text or json.")
    parser.add_argument("--depth", type=int, default=5, help="Number of levels to fetch from the order book.")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.symbol, args.delay, args.format, args.depth))
