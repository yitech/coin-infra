import json
import uuid
import logging
import websocket
import time
from confluent_kafka import Producer

class WebsocketOkexBridge:
    def __init__(self, kafka_url, kafka_topic, partition_id, exchange, symbol, websocket_url, subscribe_args):
        self.kafka_url = kafka_url
        self.kafka_topic = kafka_topic
        self.partition_id = partition_id

        self.symbol = symbol
        self.exchange = exchange
        self.websocket_url = websocket_url
        self.subscribe_args = subscribe_args
        
        self.producer = Producer({'bootstrap.servers': self.kafka_url})
        self.count = 0

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
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
        if 'event' in message and message['event'] == 'subscribe':
            # Ignore the subscription response message
            return
        message = json.loads(message)['data'][0]
        data = {
            'id': uuid.uuid4().hex,
            'symbol': self.symbol,
            'exchange': self.exchange,
            'timestamp': time.time()
            }
        data['asks'] = [[float(order[0]), float(order[1])] for order in message['asks']]
        data['bids'] = [[float(order[0]), float(order[1])] for order in message['bids']]
        self.producer.produce(self.kafka_topic, value=json.dumps(data), partition=self.partition_id)
        self.producer.flush()
        if self.count % 100 == 0:
            for key, value in data.items():
                logging.info(f"Insert data.{key}: {value}")
        self.count += 1

    @staticmethod
    def on_error(ws, error):
        logging.error("Error: %s", error)

    @staticmethod
    def on_close(ws, code, reason):
        logging.info(f"### Connection closed: {code} {reason} ###")

    def on_open(self, ws):
        # This is the request to get the orderbook with depth 5
        data = {
            "op": "subscribe",
            "args": self.subscribe_args
        }
        ws.send(json.dumps(data))
        logging.info("### Connection opened ###")

    def run(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            self.websocket_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        ws.on_open = self.on_open

        while True:
            ws.run_forever(ping_interval=5, ping_timeout=2)  # Adjust ping_interval and ping_timeout as needed
            logging.info("### Reconnecting to WebSocket ###")
            time.sleep(5)  # Adjust sleep duration as needed
