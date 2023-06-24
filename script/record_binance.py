import os
import argparse
import asyncio
import json
from datetime import datetime
from queue import Queue
from collections import defaultdict
from coin_infra.datapipe import BinanceFuturesOrderbook

class BNFOrderbookToFile(BinanceFuturesOrderbook):
    def __init__(self, wss_url, symbol, filepath, batch):
        super().__init__(wss_url, symbol)
        self.filepath = filepath
        self.batch = batch
        self.queue = Queue(maxsize=self.batch + 10)
    
    async def postprocess(self, json_data):
        await super().postprocess(json_data)
        self.queue.put(json_data)
        
        if self.queue.qsize() >= self.batch:
            cls = defaultdict(list)
            for _ in range(self.batch):
                data = self.queue.get()
                datetime_object = datetime.fromisoformat(data['timestamp'])
                time_interval = datetime_object.strftime("%Y%m%d%H")
                cls[time_interval].append(data)
            for interval, data in cls.items:
                with open(f'{self.filepath}_{interval}.log', 'a') as f:
                    for row in data:
                        f.write(json.dumps(row))
        

            

            


    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Binancefutures orderbook reader')
    parser.add_argument('json_file', type=str, help='Json file containing arguments')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        json_args = json.load(f)

    asyncio.run(main(json_args))
