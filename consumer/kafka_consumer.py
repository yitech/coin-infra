import json
import logging
from confluent_kafka import Consumer, KafkaException
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS

class KafkaConsumer:
    def __init__(self, kafka_url, kafka_group_id, kafka_topic, influx_url, influx_token, influx_org, influx_bucket):
        self.kafka_url = kafka_url
        self.kafka_group_id = kafka_group_id
        self.kafka_topic = kafka_topic
        self.influx_url = influx_url
        self.influx_token = influx_token
        self.influx_org = influx_org
        self.influx_bucket = influx_bucket

        self.kafka_conf = {
            'bootstrap.servers': self.kafka_url, 
            'group.id': kafka_group_id,
            'auto.offset.reset': 'earliest',
        }
        self.kafka_consumer = Consumer(self.kafka_conf)
        self.kafka_consumer.subscribe([self.kafka_topic])

        self.client = InfluxDBClient(url=self.influx_url, token=self.influx_token)
        self.write_api = self.client.write_api(write_options=ASYNCHRONOUS)

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

    def run(self):
        try:
            while True:
                msg = self.kafka_consumer.poll(1)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    self.process_message(msg)

        except Exception as e:
            logging.error(f'Exception occurred: {e}')

        finally:
            self.cleanup()

    def process_message(self, msg):
        data = json.loads(msg.value().decode('utf-8'))
        self.push_to_influxdb(data)
        if  self.count % 100 == 0:
            logging.info(f"Produced {data['id']}")
        self.count += 1

    def push_to_influxdb(self, data):
        point_main = Point("orderbook")
        point_main = point_main.tag("id", data["id"])
        point_main = point_main.tag("exchange", data["exchange"])
        point_main = point_main.tag("symbol", data["symbol"])
        point_main = point_main.field("timestamp", data["timestamp"])

        self.write_api.write(bucket=self.influx_bucket, org=self.influx_org, record=point_main)

        for bid in data["bids"]:
            point_bid = Point("bids")
            point_bid = point_bid.tag("id", data["id"])
            point_bid = point_bid.field("price", bid[0])
            point_bid = point_bid.field("size", bid[1])
            self.write_api.write(bucket=self.influx_bucket, org=self.influx_org, record=point_bid)
        
        for ask in data["asks"]:
            point_ask = Point("asks")
            point_ask = point_ask.tag("id", data["id"])
            point_ask = point_ask.field("price", ask[0])
            point_ask = point_ask.field("size", ask[1])
            self.write_api.write(bucket=self.influx_bucket, org=self.influx_org, record=point_ask)

    def cleanup(self):
        self.kafka_consumer.close()
        self.write_api.close()
        self.client.close()
