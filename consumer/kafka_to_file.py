import os
import json
import logging
from datetime import datetime
from confluent_kafka import Consumer, KafkaException


class KafkaToFile:
    def __init__(self, kafka_url, kafka_group_id, kafka_topic, dst_directory, batch_size):
        self.kafka_url = kafka_url
        self.kafka_group_id = kafka_group_id
        self.kafka_topic = kafka_topic

        self.kafka_conf = {
            'bootstrap.servers': self.kafka_url, 
            'group.id': kafka_group_id,
            'auto.offset.reset': 'earliest',
        }
        self.kafka_consumer = Consumer(self.kafka_conf)
        self.kafka_consumer.subscribe([self.kafka_topic])

        self.dst_directory = dst_directory
        self.batch_size = batch_size
        self.buffer = []

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
        self.buffer.append(data)
        self.count += 1
        if self.count % self.batch_size == 0:
            now = datetime.now()
            with open(f'{os.path.join(self.dst_directory, now.strftime("%Y%m%d%H"))}.txt', 'a') as outfile:
                for data in self.buffer:
                    json.dump(data, outfile)
                    outfile.write('\n')
            self.buffer.clear()
        if self.count % 100 == 0:
            for key, value in data.items():
                logging.info(f"Insert data.{key}: {value}")
        

    def cleanup(self):
        self.kafka_consumer.close()
        now = datetime.now()
        with open(f'{os.path.join(self.dst_directory, now.strftime("%Y%m%d%H"))}.txt', 'a') as outfile:
            for data in self.buffer:
                json.dump(data, outfile)
                outfile.write('\n')
        self.buffer.clear()

    


