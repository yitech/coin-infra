import argparse
import ccxt.async_support as ccxt
import logging
import asyncio
import json
import time
from datetime import datetime

# Creating a custom logger
logger = logging.getLogger(__name__)

# Setting log format
logging.basicConfig(format='[%(asctime)s][%(filename)s:%(lineno)d][%(message)s]', level=logging.INFO)

async def get_orderbook(config_path):

    # Load the config
    with open(config_path) as f:
        config = json.load(f)

    exchange = ccxt.binance({
        'apiKey': config['apiKey'],
        'secret': config['secret']
    })

    # Asynchronously fetch orderbook
    try:
        orderbook = await exchange.fetch_order_book('BTC/USDT')
        logger.info("Orderbook: %s", orderbook)
    except Exception as e:
        logger.exception("An error occurred while fetching the order book.")
    finally:
        # Close the session gracefully.
        await exchange.close()

async def main(config_path):

    while True:
        try:
            await get_orderbook(config_path)
            await asyncio.sleep(1)  # Adding delay for continuous running.
        except Exception as e:
            logger.exception("An error occurred: restarting...")
            await asyncio.sleep(5)  # Wait 5 seconds before restart

if __name__ == "__main__":
    # Using argparse to input config path
    parser = argparse.ArgumentParser(description="Fetch BTC/USDT orderbook")
    parser.add_argument('--config_path', required=True, help='Path to config file')
    args = parser.parse_args()

    # Async IO event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.config_path))
