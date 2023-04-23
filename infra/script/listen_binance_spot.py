import asyncio
import ccxt.async_support as ccxt

async def main():
    binance = ccxt.binance({
        'enableRateLimit': True,
    })

    while True:
        try:
            ticker = await binance.fetch_ticker('BTC/USDT')
            print("Symbol: {}, Bid: {}, Ask: {}".format(
                ticker['symbol'], ticker['bid'], ticker['ask']
            ))
            await asyncio.sleep(5)  # Adjust the delay as needed.
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)
        finally:
            await binance.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
