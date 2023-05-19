import os
from fastapi import FastAPI
import asyncio
import aiohttp
import json
import time
from confluent_kafka import Producer

# Parse command-line arguments
config_path = os.environ.get('CONFIG_PATH')

# Read the configuration file
with open(config_path, 'r') as f:
    config = json.load(f)

app = FastAPI()

# Initialize the Kafka Producer
p = Producer({'bootstrap.servers': config['kafka_url']})

# Function to handle Kafka delivery reports
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

async def fetch_data(session, url1, url2):
    try:
        orderbook1
        async with session.get(url) as resp:
            data = await resp.text()
            return json.loads(data)
    except Exception as e:
        print(f"Failed to fetch from {url}: {e}")
        return None

def publish_data(data):
    if data is not None:
        p.produce(config['topic'], value=json.dumps(data), callback=delivery_report)
        p.poll(0) # This line is important for the Producer to serve delivery callbacks


async def fetch_and_publish(session, endpoints):
    data = await fetch_data(session, endpoints)
    publish_data(data)


class Listener:
    def __init__(self, endpoints):
        self.endpoints = endpoints
        self.task = None

    async def start(self):
        if self.task is None:
            self.task = asyncio.create_task(self._run())

    async def stop(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

    async def _run(self):

        while True:
            async with aiohttp.ClientSession() as session:
                await fetch_and_publish(session, self.endpoints)
                time.sleep(config["sleep"])  # Sleep for one second

listener = Listener(config["endpoints"])

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
