import websockets
import json
from datetime import datetime, timezone
import hashlib
import traceback
from coin_infra.core import Logger

class BinanceFuturesOrderbook:
    def __init__(self, wss_url, symbol):
        self.wss_url = wss_url
        self.symbol = symbol
        self.logger = Logger(__name__ + wss_url)
    
  
    async def process_message(self, message):
        try:
            json_data = json.loads(message)
            dt_object = datetime.fromtimestamp(json_data["T"] / 1000, timezone.utc)
            unique_pattern = f"binancefuture{json_data['E']}{json_data['s']}"
            json_data = {"id": hashlib.sha256(unique_pattern.encode()).hexdigest(), 
                         "symbol": self.symbol, 
                         "timestamp": dt_object.isoformat(),
                         "exchange": "binance",
                         'ask': [[float(item) for item in sublist] for sublist in json_data['a']], 
                         'bid': [[float(item) for item in sublist] for sublist in json_data['b']]}
            return json_data
        except Exception as e:
            self.logger.info(f"{e}: {traceback.format_exc()}")
            exit()
    
    async def postprocess(self, json_data):
        self.logger.info(json_data)


    async def run(self):
        async with websockets.connect(self.wss_url) as websocket:
            async for message in websocket:
                json_data = await self.process_message(message)
                await self.postprocess(json_data)
                
