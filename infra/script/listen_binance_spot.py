import asyncio
import ccxt.async_support as ccxt
import argparse

async def main(symbol, delay):
    binance = ccxt.binance({
        'enableRateLimit': True,
    })

    while True:
        try:
            ticker = await binance.fetch_ticker(symbol)
            print("Symbol: {}, Bid: {}, Ask: {}".format(
                ticker['symbol'], ticker['bid'], ticker['ask']
            ))
            await asyncio.sleep(delay)  # Adjust the delay as needed.
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(delay)
        finally:
            await binance.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor the spot price of a trading pair on Binance.")
    parser.add_argument("symbol", help="Trading pair symbol (e.g., BTC/USDT).")
    parser.add_argument("delay", type=int, help="Time delay between price fetches in seconds.")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.symbol, args.delay))
