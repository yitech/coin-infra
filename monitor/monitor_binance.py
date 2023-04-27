# python monitor_binance.py BTC/USDT 5 --format json --depth 3
import asyncio
import ccxt.async_support as ccxt
import argparse
import json

async def main(symbol, delay, output_format, depth):
    binance = ccxt.binance({
        'enableRateLimit': True,
    })

    while True:
        try:
            order_book = await binance.fetch_order_book(symbol, depth)

            bids = order_book['bids']
            asks = order_book['asks']

            if output_format == 'json':
                print(json.dumps({
                    'symbol': symbol,
                    'bids': bids,
                    'asks': asks,
                }))
            else:
                print(f"Symbol: {symbol}")
                print("Bids:")
                for price, size in bids:
                    print(f"Price: {price}, Size: {size}")
                print("Asks:")
                for price, size in asks:
                    print(f"Price: {price}, Size: {size}")

            await asyncio.sleep(delay)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(delay)
        finally:
            await binance.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor the spot price of a trading pair on Binance.")
    parser.add_argument("symbol", help="Trading pair symbol (e.g., BTC/USDT).")
    parser.add_argument("delay", type=int, help="Time delay between price fetches in seconds.")
    parser.add_argument("--format", choices=['text', 'json'], default='text', help="Output format: text or json.")
    parser.add_argument("--depth", type=int, default=5, help="Number of levels to fetch from the order book.")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.symbol, args.delay, args.format, args.depth))
