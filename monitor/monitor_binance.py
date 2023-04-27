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


