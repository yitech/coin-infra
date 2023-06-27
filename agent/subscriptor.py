import argparse
import json
import redis
import traceback
from urllib.parse import urlparse
from pymongo import MongoClient
from queue import Queue
from coin_infra.core import Logger

class Consumer:
    def __init__(self, redis_url, channel, mongo_url):
        parsed = urlparse(redis_url)
        host = parsed.hostname
        port = parsed.port
        self.redis_conn = redis.Redis(host, port)
        self.channel = channel

        parsed = urlparse(mongo_url)
        protocol_host = parsed.scheme + "://" + parsed.hostname
        port = parsed.port
        self.mongo_client = MongoClient(protocol_host, port)

        self.queue = Queue()
        self.logger = Logger(__name__)

    def consume(self):
        try:
            pubsub = self.redis_conn.pubsub()
            pubsub.subscribe(self.channel)
            
            # Skip the first message (the subscription confirmation)
            confirmation =  next(pubsub.listen())
            self.logger.info(f'Confirmation: {confirmation}')

            for message in pubsub.listen():
                data = json.loads(message['data'].decode('utf-8'))
                self.logger.info(f'{data=}')
                
                
        except Exception as e:
            self.logger.info(f'Error occurred: {traceback.format_exc()}')
        finally:
            pubsub.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Binancefutures orderbook reader')
    parser.add_argument('json_file', type=str, help='Json file containing arguments')
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        json_args = json.load(f)
    
    broker = json_args['broker']
    mongo = json_args['mongo']

    sub = Consumer(broker['url'], broker['channel'], mongo['url'])
    sub.consume()

