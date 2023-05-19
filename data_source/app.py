import datetime
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

# The Kafka configuration, change as needed
kafka_config = {
    'bootstrap.servers': config['kafka_url']
}
topic = 'your_topic'

# The URL to request data from every second
url = 'http://example.com/your_endpoint'



async def fetch(session, url):
    print(f"Fetching URL: {url}")
    async with session.get(url) as response:
        data = await response.json()
        print(f"Data fetched from {url}: {data}")
        return data

async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

def send_to_kafka(data):
    conf = {'bootstrap.servers': config['kafka_url']}
    producer = Producer(conf)

    for i, item in enumerate(data):
        print(f"Sending data_{i} to Kafka: {item}")
        producer.produce(config['topic'], key=f'data_{i}', value=json.dumps(item))

    print("Data sent to Kafka, waiting for it to be written...")
    producer.flush()
    print("Data written to Kafka successfully.")


async def main():
    urls = list(config['endpoints'].values())
    while True:
        loop = asyncio.get_event_loop()
        print("Starting to fetch data from URLs...")
        htmls = await fetch_all(urls, loop)
        print("Finished fetching data, sending to Kafka...")
        send_to_kafka(htmls)
        print("Sleeping for 1 second before next fetch...")
        await asyncio.sleep(1)  # Sleep for a second

loop = asyncio.get_event_loop()
try:
    print("Starting main loop...")
    loop.run_until_complete(main())
finally:
    print("Closing main loop...")
    loop.close()