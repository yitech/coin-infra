
import argparse
import json
import uuid
import asyncio
import aiohttp
from datetime import datetime
from confluent_kafka import Producer
import logging
import time
import traceback
import concurrent.futures

logging.basicConfig(format='[%(asctime)s][%(filename)s:%(lineno)d][%(message)s]', level=logging.INFO)

def delivery_report(err, msg):
        if err is not None:
            logging.info(f"Message delivery failed: {err}")
        else:
            logging.info(f"Message delivered to {msg.topic()}")

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.json()

def push_to_kafka(producer, topic, data, metadata):
    data.update(metadata)
    data['id'] = uuid.uuid4().hex
    producer.produce(topic, json.dumps(data), callback=delivery_report)
    producer.poll(0)
    logging.info(f"Pushed {data['id']} to Kafka topic: {topic}")

async def main(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    url = config['url']
    producer = Producer({'bootstrap.servers': config['kafka_url']})
    metadata = {
        'exchange': config['exchange']
        }
    
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # Compute time until next second
                current_time = time.time()
                sleep_time = 1 - (current_time % 1)
                await asyncio.sleep(sleep_time)

                response = await fetch_url(session, url)
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    await asyncio.get_event_loop().run_in_executor(pool, push_to_kafka, producer, config['topic'], response, metadata)
                
                
            except Exception as e:
                logging.error(f"Error occurred: {e}")
                logging.error(traceback.format_exc())
                logging.info("Restarting...")
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Config file path")
    args = parser.parse_args()
    asyncio.run(main(args.config))
