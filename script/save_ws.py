import json
import asyncio
import websockets

BATCH_SIZE = 5  # Set this to an appropriate value

async def listen(url):
    async with websockets.connect(url) as websocket:
        while True:
            data = await websocket.recv()
            yield data

async def main():
    url = 'wss://fstream.binance.com/ws/btcusdt@depth5@500ms'  # Replace with your WebSocket url
    batch = []
    try:
        async for message in listen(url):
            json_data = json.loads(message)
            batch.append(json_data)
            if len(batch) >= BATCH_SIZE:
                with open('data.json', 'a') as outfile:
                    for data in batch:
                        json.dump(data, outfile)
                        outfile.write('\n')
                batch = []
    except KeyboardInterrupt:
        # Write the remaining data in the last batch to the file when KeyboardInterrupt is raised
        if batch:
            with open('data.json', 'a') as outfile:
                for data in batch:
                    json.dump(data, outfile)
                    outfile.write('\n')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())