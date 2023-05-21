import os
import sys
import json
import argparse
import logging
import time
from confluent_kafka import Consumer, KafkaException
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS

# Initialize logging
log_format = '[%(asctime)s][%(filename)s: %(lineno)d][%(message)s]'
logging.basicConfig(level=logging.INFO, format=log_format)

def main(config_path):
    # Read the configuration file
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Set up Kafka consumer
    kafka_conf = {
        'bootstrap.servers': config['kafka_url'], # adapt to your Kafka setup
        'group.id': config['group_id'],
        'auto.offset.reset': 'earliest',
    }
    c = Consumer(kafka_conf)

    # Subscribe to Kafka topic
    c.subscribe([config['topic']])  # replace 'my-topic' with your topic

    # Set up InfluxDB client
    influx_conf = {
        'url': config['influx_url'],
        'token': config['influx_token'],
        'org': config['influx_org'],
        'bucket': config['influx_bucket']
    }

    client = InfluxDBClient(url=influx_conf['url'], token=influx_conf['token'])
    write_api = client.write_api(write_options=ASYNCHRONOUS)
    count = 0
    try:
        while True:
            msg = c.poll(1)  # Poll Kafka for messages
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Parse Kafka message
                data = json.loads(msg.value().decode('utf-8'))  # assuming messages are JSON
                logging.info(f"Consumer {data['id']}...")
                
                # Prepare data for InfluxDB
                point_main = Point("orderbook")
                point_main = point_main.tag("id", data["id"])
                point_main = point_main.tag("exchange", data["exchange"])
                point_main = point_main.tag("symbol", data["symbol"])
                point_main = point_main.field("timestamp", data["timestamp"])

                write_api.write(bucket=influx_conf['bucket'], org=influx_conf['org'], record=point_main)

                for bid in data["bids"]:
                    point_bid = Point("bids")
                    point_bid = point_bid.tag("id", data["id"])
                    point_bid = point_bid.field("price", bid[0])
                    point_bid = point_bid.field("size", bid[1])
                    write_api.write(bucket=influx_conf['bucket'], org=influx_conf['org'], record=point_bid)
                
                for ask in data["asks"]:
                    point_ask = Point("asks")
                    point_ask = point_ask.tag("id", data["id"])
                    point_ask = point_ask.field("price", ask[0])
                    point_ask = point_ask.field("size", ask[1])
                    write_api.write(bucket=influx_conf['bucket'], org=influx_conf['org'], record=point_ask)

    except Exception as e:
        logging.error(f'Exception occurred: {e}')
        time.sleep(5)  # Sleep for 5 seconds before auto-restart
        main(config_path)
    
    finally:
        c.close()
        write_api.close()
        client.close()


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration file')
    args = parser.parse_args()
    main(args.config)
