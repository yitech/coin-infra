import os
import argparse
import asyncio
import json
import aioredis
import traceback
from datetime import datetime
from queue import Queue
from collections import defaultdict
from coin_infra.datapipe import BinanceFuturesOrderbook

class BNFOrderbookToRedis(BinanceFuturesOrderbook):
    def __init__(self, wss_url, symbol, redis_url, channel):
        super().__init__(wss_url, symbol)
        self.redis_url = redis_url
        self.channel = channel
        self.redis = None

    async def init_redis(self):
        self.redis = await aioredis.from_url(self.redis_url)
    
    async def postprocess(self, json_data):
        # await super().postprocess(json_data)
        json_string = json.dumps(json_data)
        try:
            # Use await to push the data into the Redis database.
            await self.redis.publish(self.channel, json_string)
        except Exception as e:
            self.logger.error(f' {e} : {traceback.format_exc()}')
            await self.stop()


    async def run(self):
        # Add initialization of the Redis connection to the run method.
        await self.init_redis()
        await super().run()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Binancefutures orderbook reader')
    parser.add_argument('json_file', type=str, help='Json file containing arguments')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        json_args = json.load(f)

    bnf = BNFOrderbookToRedis(json_args['wss'], json_args['symbol'], json_args['redis_url'], json_args['channel'])
    asyncio.run(bnf.run())
