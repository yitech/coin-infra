from datetime import datetime,  timedelta
import os
import asyncio
import aiohttp
import json
import uuid
from confluent_kafka import Producer, KafkaError

# Parse command-line arguments
config_path = os.environ.get('CONFIG_PATH')
config_path = 'config_test.json'

# Read the configuration file
with open(config_path, 'r') as f:
    config = json.load(f)

print(f"Configuration: {config}")

# The Kafka configuration, change as needed
kafka_config = {
    'bootstrap.servers': config['kafka_url']
}
topic = config['topic']

# The URL to request data from every second
url = config['endpoint']

# The flush timeout, in seconds
flush_timeout = 10.0

async def sub_pub_data(session, url, producer, metadata):
    metadata.update({'id': uuid.uuid4().hex})
    async with session.get(url) as resp:
        data = await resp.json()
        print(f"Received data: {data}")
        data.update(metadata)
        print(f"Data after adding metadata: {data}")
        producer.produce(topic, json.dumps(data).encode('utf-8'))
        result = producer.flush(timeout=flush_timeout)
        if result > 0:
            raise KafkaError("Failed to flush all messages within the given timeout")
        else:
            print(f"Successfully produced message to Kafka topic: {topic}")

async def main():
    producer = Producer(kafka_config)
    metadata = {
        'exchange': config['exchange'],
        'symbol': config['symbol']
    }
    async with aiohttp.ClientSession() as session:
        while True:
            now = datetime.now()
            print(f"Current time: {now}")
            trigger_time = (now + timedelta(seconds=1)).replace(microsecond=0)
            await asyncio.sleep((trigger_time - now).total_seconds())
            print(f"Fetching data at: {datetime.now()}")
            await sub_pub_data(session, url, producer, metadata)
            

# Run the main function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
