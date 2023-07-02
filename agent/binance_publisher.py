import argparse
import json
import aioredis
import asyncio
import traceback
from queue import Queue
from urllib.parse import urlparse
from motor.motor_asyncio import AsyncIOMotorClient
from coin_infra.core import Logger
from datetime import datetime
from collections import defaultdict

class Consumer:
    def __init__(self, redis_url, channel, mongo_url):
        self.redis_url = redis_url
        self.channel = channel
        self.mongo_url = mongo_url
        self.queue = Queue()
        self.logger = Logger(__name__)

    async def init_connections(self):
        self.redis_conn = await aioredis.from_url(self.redis_url)
        self.mongo_client = AsyncIOMotorClient(self.mongo_url)

    async def commit_to_mongo(self, data):
        # parse date from timestamp
        await self.queue.put(data)  # Put data in queue
        
        if self.queue.qsize() > 1000:
            self.logger.info(f'{self.queue.qsize()=}')
            data_batch = defaultdict(list)
            for _ in range(1000):
                data = self.queue.get()
                dt = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')
                date = dt.strftime('%Y-%m-%d')
                data_batch[date].append(data)
            
            # use the date as the collection name
            for date, data in data_batch.items():
                collection = self.mongo_client['orderbook'][date]
                # insert the data into the collection
                await collection.insert_many(data)

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
                    # commit the data to MongoDB
                    await self.commit_to_mongo(data)
                else:
                    await asyncio.sleep(1)  # wait for a second if no message

        except Exception as e:
            self.logger.error(f'Error occurred: {traceback.format_exc()}')

        finally:
            await pubsub.unsubscribe(self.channel)
            self.redis_conn.close()
            await self.redis_conn.wait_closed()