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
        filename = f"OKEX_{symbol.replace('/', '_')}_{formatted}.txt"
        outfile = os.path.join(outdir, filename)
        with open(outfile, 'a') as f:
            for data in batch:
                json.dump(data, f)
                f.write('\n')
            batch.clear()


async def main(args):
    queue = asyncio.Queue()
    WS_ADDRESS = args["websocket_url"]

    while True:
        try:
            async with websockets.connect(WS_ADDRESS) as websocket:
                dump_task = asyncio.create_task(dump_to_file(args["outdir"], args["symbol"], args["batch_size"], queue))
                # Send subscription message
                data = json_args["request"]
                await websocket.send(json.dumps(data))
                response = await websocket.recv()
                logging.info(f"Received response: {response}")
                async for message in websocket:
                    try:
                        json_data = json.loads(message)['data'][0]
                        dt_object = datetime.fromtimestamp(int(json_data["ts"]) / 1000, timezone.utc)
                        json_data = {"id": uuid.uuid4().hex, 
                                     "symbol": args["symbol"], 
                                     "timestamp": dt_object.isoformat(),
                                     "exchange": "okex",
                                     'ask': [[float(item) for item in sublist[:2]] for sublist in json_data['asks']], 
                                     'bid': [[float(item) for item in sublist[:2]] for sublist in json_data['bids']]}
                    except json.JSONDecodeError:
                        logging.error('JSONDecodeError for message: %s', message)
                        continue
                    await queue.put(json_data)
                break  # if all goes well, break out of the reconnection loop
        except Exception as e:
            logging.error('WebSocket connection error: %s', str(e))
            logging.info('Reconnecting in 60 seconds...')
            await asyncio.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Websocket reader and json dumper.')
    parser.add_argument('json_file', type=str, help='Json file containing arguments')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        json_args = json.load(f)

    asyncio.run(main(json_args))
