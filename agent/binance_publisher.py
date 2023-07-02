import os
import time
import argparse
import asyncio
import json
from datetime import datetime
from queue import Queue
from collections import defaultdict
from coin_infra.datapipe import BinanceFuturesOrderbook

class BinanceOrderbookPub(BinanceFuturesOrderbook):
    def __init__(self, wss_url, symbol, redis_url, channel):
        super().__init__(wss_url, symbol)
        self.redis_url = redis_url
        self.channel = channel
    
    async def postprocess(self, json_data):
        await super().postprocess(json_data)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Binancefutures orderbook reader')
    parser.add_argument('json_file', type=str, help='Json file containing arguments')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        json_args = json.load(f)

    pub = json_args['pub']
    broker = json_args['broker']

    binance = BinanceOrderbookPub(pub['wss'], pub['symbol'], broker['url'], broker['channel'])
    asyncio.run(binance.run())

    
    
