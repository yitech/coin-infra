from fastapi import FastAPI
import asyncio
import aiohttp
import json
import time
from confluent_kafka import Producer

app = FastAPI()

# Initialize the Kafka Producer
p = Producer({'bootstrap.servers': 'kafka-kafka-1:9092'})

# Function to handle Kafka delivery reports
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

async def fetch_data(session, url):
    try:
        async with session.get(url) as resp:
            data = await resp.text()
            return json.loads(data)
    except Exception as e:
        print(f"Failed to fetch from {url}: {e}")
        return None

def publish_data(data):
    if data is not None:
        p.produce('bitcoin_ticker', value=json.dumps(data), callback=delivery_report)
        p.poll(0) # This line is important for the Producer to serve delivery callbacks

async def fetch_and_publish(session, url):
    data = await fetch_data(session, url)
    publish_data(data)

class Listener:
    def __init__(self, symbol):
        self.symbol = symbol
        self.task = None

    async def start(self):
        if self.task is None:
            self.task = asyncio.create_task(self._run())

    async def stop(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

    async def _run(self):
        endpoints = [
            f"http://binancefuture:40000/ticker?symbol={self.symbol}",
            f"http://okxfuture:40001/ticker?symbol={self.symbol}"
        ]

        while True:
            async with aiohttp.ClientSession() as session:
                tasks = []
                for endpoint in endpoints:
                    tasks.append(fetch_and_publish(session, endpoint))
                await asyncio.gather(*tasks)
                time.sleep(1)  # Sleep for one second

listener = Listener('BTC/USDT')

@app.on_event("shutdown")
async def shutdown_event():
    await listener.stop()
    p.flush()

@app.get("/start")
async def start_listener():
    await listener.start()
    return {"status": "Started listener"}

@app.get("/stop")
async def stop_listener():
    await listener.stop()
    return {"status": "Stopped listener"}
