import asyncio
from pymongo.errors import ServerSelectionTimeoutError
from pymongo import MongoClient
import ccxt.async_support as ccxt_async
from datetime import datetime


def connect_to_mongodb():
    try:
        client = MongoClient(
            "mongodb+srv://coin-time-series.rvdyfea.mongodb.net/?"
            "authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
            , serverSelectionTimeoutMS=5000)
        client.server_info()  # Will raise an exception if it cannot connect
    except ServerSelectionTimeoutError as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    return client

async def record(exchange, client, symbol, delay, depth):
    # Connect to the database and collection
    db = client['coin']
    collection = db['price']

    while True:
        try:
            ticker = await exchange.fetch_ticker(symbol)
            orderbook = await exchange.fetch_order_book(symbol, limit=depth)
            bids = orderbook['bids']
            asks = orderbook['asks']

            data = {
                'timestamp': datetime.now().timestamp()
                'exchange': exchange.name,
                'symbol': symbol,
                'price': ticker['last'],
                'bids': bids,
                'asks': asks,
            }

            # Insert the data into MongoDB
            result = collection.insert_one(data)
            print(f"Inserted document with ID: {result.inserted_id}")

            await asyncio.sleep(delay)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)


async def run():
    symbol = "BTC/USDT"
    api_key = {'binance': 'your_api_key',
               'okx': '5b26a0c1-cf08-4815-af1c-bb8a4688678a'}
    api_secret = {'binance': 'your_api_secret',
                  'okx': 'ED7C623550788523A14CE060CDAD40FD'}

    binance = ccxt_async.binance({
        # 'apiKey': api_key['binance'],
        # 'secret': api_secret['binance'],
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        },
    })

    okx = ccxt_async.okx({
        'apiKey': api_key['okx'],
        'secret': api_secret['okx'],
        'enableRateLimit': True,
    })

    # Connect to MongoDB
    client = connect_to_mongodb()

    await asyncio.gather(
        record(binance, client, 1, symbol, 10),
        record(okx, client, 1, symbol, 10)
    )

if __name__ == "__main__":
    # Create an asyncio event loop and run the run_multiple_mains function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())