import os
import argparse
import asyncio
import websockets
import json
from datetime import datetime, timezone
import hashlib
from core import Logger

class BinanceFuturesOrderbook:
    def __init__(self, wss_url):
        self.wss_url = wss_url
        self.logger = Logger(__name__)
    
  
    async def process_message(self, message):
        try:
            json_data = json.loads(message)
        except json.JSONDecodeError:
            self.Logger.error('JSONDecodeError for message: %s', message)
            return None

        dt_object = datetime.fromtimestamp(json_data["T"] / 1000, timezone.utc)
        json_data = {"id": hashlib.sha256((str(json_data["E"]) + json_data["s"]).encode()).hexdigest(), 
                     "symbol": 'LTC', 
                     "timestamp": dt_object.isoformat(),
                     "exchange": "binance",
                     'ask': [[float(item) for item in sublist] for sublist in json_data['a']], 
                     'bid': [[float(item) for item in sublist] for sublist in json_data['b']]}
        return json_data

    async def run(self):
        WS_ADDRESS = self.wss_url
        async with websockets.connect(WS_ADDRESS) as websocket:
            async for message in websocket:
                self.logger.info(message)
                json_data = await self.process_message(message)
                self.logger.info(json_data)


if __name__ == "__main__":
    reader = BinanceFuturesOrderbook('wss://fstream.binance.com/ws/ltcusdt@depth5@100ms')
    asyncio.run(reader.run())
