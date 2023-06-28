import argparse
import json
import aioredis
import asyncio
import traceback
from urllib.parse import urlparse
from motor.motor_asyncio import AsyncIOMotorClient
from coin_infra.core import Logger

class Consumer:
    def __init__(self, redis_url, channel, mongo_url):
        self.redis_url = redis_url
        self.channel = channel
        self.mongo_url = mongo_url
        self.queue = asyncio.Queue()
        self.logger = Logger(__name__)

    async def init_connections(self):
        self.redis_conn = await aioredis.from_url(self.redis_url)
        self.mongo_client = AsyncIOMotorClient(self.mongo_url)

    async def consume(self):
        try:
            await self.init_connections()

            pubsub = self.redis_conn.pubsub()
            channel = await pubsub.subscribe(self.channel)
            self.logger.info(f'Subscribed to {self.channel}')

            # Skip the first message (the subscription confirmation)
            confirmation = await pubsub.get_message()
            self.logger.info(f'Confirmation: {confirmation}')

            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    data = json.loads(message['data'].decode('utf-8'))
                    self.logger.info(f'{data=}, {self.queue.qsize()}')
                    await self.queue.put(data)  # Put data in queue
                else:
                    await asyncio.sleep(1)  # wait for a second if no message

        except Exception as e:
            self.logger.error(f'Error occurred: {traceback.format_exc()}')

        finally:
            await pubsub.unsubscribe(self.channel)
            self.redis_conn.close()
            await self.redis_conn.wait_closed()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Binancefutures orderbook reader')
    parser.add_argument('json_file', type=str, help='Json file containing arguments')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        json_args = json.load(f)
    
    broker = json_args['broker']
    mongo = json_args['mongo']

    sub = Consumer(broker['url'], broker['channel'], mongo['url'])
    asyncio.run(sub.consume())
