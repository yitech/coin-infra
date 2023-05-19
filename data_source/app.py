from datetime import datetime, timedelta
import os
import asyncio
import aiohttp
import json
import uuid
from confluent_kafka import Producer

# Parse command-line arguments
config_path = os.environ.get('CONFIG_PATH')

# Read the configuration file
with open(config_path, 'r') as f:
    config = json.load(f)

# Kafka Producer
producer = Producer({'bootstrap.servers': config['kafka_url']})

async def get_url(session, url):
    async with session.get(url) as response:
        return await response.json()

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

async def main():
    async with aiohttp.ClientSession() as session:
        #  Schedule the first call to wait(
        interval = 1 / config['frequency']
        trigger = (datetime.now() + timedelta(seconds=2)).replace(microsecond=0)
        wait = datetime.now() - trigger 
        await asyncio.sleep(wait.total_seconds())
        metadata = {
            "_id": uuid.uuid4().hex,
            "exchange": config["exchange"],
            "symbol": config["symbol"]
        }
        
        while True:
            for _ in range(int(config['frequency']) - 1):
                data = await get_url(session, config['endpoint'])
                data.update(metadata)
                await asyncio.sleep(interval)
                # Trigger any available delivery report callbacks from previous produce() calls
                producer.poll(0)

                # Asynchronously produce a message, the delivery report callback
                # will be triggered from poll() above, or flush() below, when the message has
                # been successfully delivered or failed permanently.
                producer.produce(config['topic'], key=config['exchange'], value=json.dumps(data).encode('utf-8'), callback=delivery_report)

                # Wait for any outstanding messages to be delivered and delivery reports
                # to be triggered.
                producer.flush()
            trigger = (datetime.now() + timedelta(seconds=1)).replace(microsecond=0)
            wait = datetime.now() - trigger 
            # Wait for the next call to wait()
            await asyncio.sleep(wait.total_seconds())
            

# Run the main function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())