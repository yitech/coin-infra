import websockets
import json
from datetime import datetime, timezone
import hashlib
import traceback
from coin_infra.core import Logger

class OkexOrderbook:
    def __init__(self, wss_url, symbol):
        self.wss_url = wss_url
        self.symbol = symbol
        self.logger = Logger(__name__ + wss_url)
    
  
    async def process_message(self, message):
        try:
            message = json.loads(message)
            arg = message['arg']
            data = message['data'][0]
            unique_pattern = f"okx{data['seqId']}{arg['instId']}"
            json_data = {"id": hashlib.sha256(unique_pattern.encode()).hexdigest(),
                         "symbol": self.symbol, 
                         "timestamp": int(data['ts']),
                         "exchange": "okex",
                         'ask': [[float(item) for item in sublist[:2]] for sublist in data['asks']], 
                         'bid': [[float(item) for item in sublist[:2]] for sublist in data['bids']]}
            json_data = json.dumps(json_data)
            return json_data
        except Exception as e:
            self.logger.info(f"{e}: {traceback.format_exc()}")
            exit()

    async def run(self, subscription):
        async with websockets.connect(self.wss_url) as websocket:
            await websocket.send(json.dumps(subscription))
            response = await websocket.recv()
            self.logger.info(response)
            async for message in websocket:
                json_data = await self.process_message(message)
                self.logger.info(json_data)

