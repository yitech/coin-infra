import csv
import json
import os
import logging
from datetime import datetime, timezone, timedelta

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

def convert_to_orderbook(soruce_directory, date):
    orderbook = open('orderbook.csv', 'w')
    orderbook_writer = csv.writer(orderbook)
    asks = open('asks.csv', 'w')
    orderbook_writer.writerow(['id', 'timestamp', 'symbol', 'exchange'])
    asks_writer = csv.writer(asks)
    asks_writer.writerow(['id', 'price', 'size'])
    bids = open('bids.csv', 'w')
    bids_writer = csv.writer(bids)
    bids_writer.writerow(['id', 'price', 'size'])
    for root, dirs, files in os.walk(soruce_directory):
        for file in files:
            logging.info(f"Processing {file}")
            src = os.path.join(root, file)
            with open(src, 'r') as log:
                line = log.readline()
                while line:
                    data = json.loads(line)
                    timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
                    if date == timestamp.date():
                        orderbook_writer.writerow([data['id'], data['timestamp'], data['symbol'], data['exchange']])
                        for price, size in data['asks']:
                            asks_writer.writerow([data['id'], price, size])
                        for price, size in data['bids']:
                            bids_writer.writerow([data['id'], price, size])
                    line = log.readline()
    orderbook.close()
    asks.close()
    bids.close()

if __name__ == "__main__":
    date = datetime.fromisoformat("2023-05-28T13:27:54.088343+00:00".replace('Z', '+00:00')).date()
    # date = datetime.today() - timedelta(days=1)
    convert_to_orderbook('coin_data_2', date)