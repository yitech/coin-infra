import json
import uuid
import logging
import websocket
from confluent_kafka import Producer
import time

class WebsocketKafkaBridge:
    def __init__(self, karfka_url, kafka_topic, partition_id, exchange, symbol, websocket_url):
        self.kafka_url = karfka_url
        self.kafka_topic = kafka_topic
        self.partition_id = partition_id
        
        self.symbol = symbol
        self.exchange = exchange
        self.websocket_url = websocket_url
        
        self.producer = Producer({'bootstrap.servers': self.kafka_url})
        self.count = 0

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",  # removed the space between '%' and '(message)s'
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    @staticmethod
    def read_config_file(path):
        with open(path, 'r') as f:
            config = json.load(f)
        for key, value in config.items():
            logging.info(f"{key}: {value}")
        return config

    def on_message(self, ws, message):
        message = json.loads(message)
        message['symbol'] = self.symbol
        message['exchange'] = self.exchange
        message['id'] = uuid.uuid4().hex
        message['timestamp'] = time.time()
        
        self.producer.produce(self.kafka_topic, value=json.dumps(message), partition=self.partition_id)
        self.producer.flush()
        if  self.count % 100 == 0:
            logging.info(f"Produced {message['id']}")
        self.count += 1
        

    @staticmethod
    def on_error(ws, error):
        logging.error("Error: %s", error)

    @staticmethod
    def on_close(ws):
        logging.info("### Connection closed ###")

    @staticmethod
    def on_open(ws):
        logging.info("### Connection opened ###")

    def run(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            self.websocket_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()