import os
import argparse
import asyncio
import logging
import websockets
import json
from datetime import datetime, timezone
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

async def dump_to_file(outdir, symbol, batch_size, queue):
    batch = []
    while True:
        while len(batch) < batch_size:
            data = await queue.get()
            batch.append(data)
        formatted = datetime.now().strftime("%Y%m%d%H")
        filename = f"BINANCE_{symbol.replace('/', '_')}_{formatted}.txt"
        outfile = os.path.join(outdir, filename)
        with open(outfile, 'a') as f:
            for data in batch:
                json.dump(data, f)
                f.write('\n')
            batch.clear()

async def main(args):
    queue = asyncio.Queue()
    WS_ADDRESS = args["websocket_url"]
    try:
        async with websockets.connect(WS_ADDRESS) as websocket:
            dump_task = asyncio.create_task(dump_to_file(args["outdir"], args["symbol"], args["batch_size"], queue))
            async for message in websocket:
                try:
                    json_data = json.loads(message)
                    dt_object = datetime.fromtimestamp(json_data["T"] / 1000, timezone.utc)
                    json_data = {"id": uuid.uuid4().hex, 
                                 "symbol": args["symbol"], 
                                 "timestamp": dt_object.isoformat(),
                                 "exchange": "binance",
                                 'ask': [[float(item) for item in sublist] for sublist in json_data['a']], 
                                 'bid': [[float(item) for item in sublist] for sublist in json_data['b']]}
                except json.JSONDecodeError:
                    logging.error('JSONDecodeError for message: %s', message)
                    continue
                await queue.put(json_data)
    except KeyboardInterrupt:
        # Final dump when KeyboardInterrupt is raised
        await dump_task

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Websocket reader and json dumper.')
    parser.add_argument('json_file', type=str, help='Json file containing arguments')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        json_args = json.load(f)

    asyncio.run(main(json_args))