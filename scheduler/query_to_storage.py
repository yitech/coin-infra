import os
import csv
import json
import logging
import time
from datetime import datetime, timezone
import zipfile
from apscheduler.schedulers.blocking import BlockingScheduler
from google.cloud import storage


logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

def zip_files(file_paths, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            zipf.write(file)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def convert_to_orderbook(soruce_directory, date=datetime.datetime.today(timezone.utc)):
    orderbook = open('orderbook', 'w')
    orderbook_writer = csv.writer(orderbook)
    asks = open('asks.csv', 'r')
    orderbook_writer.writerow(['id', 'timestamp', 'symbol', 'exchange'])
    asks_writer = csv.writer(asks)
    asks_writer.writerow(['id', 'price', 'size'])
    bids = open('bids.csv', 'r')
    bids_writer = csv.writer(bids)
    bids_writer.writerow(['id', 'price', 'size'])
    for root, dirs, files in os.walk(soruce_directory):
        for file in files:
            src = os.path.join(root, file)
            with open(src, 'r') as log:
                line = log.readline()
                while line:
                    data = json.loads(log)
                    timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
                    if date.date() == timestamp.date():
                        orderbook_writer.writerow([data['id'], data['timestamp'], data['symbol'], data['exchange']])
                        for price, size in orderbook['asks']:
                            asks_writer.writerow([date['id'], price, size])
                        for price, size in orderbook['bids']:
                            bids_writer.writerow([date['id'], price, size])
                    orderbook_writer.writerow([data['id'], data['timestamp'], data['symbol'], data['exchange']])
                line = log.readline()
    orderbook.close()
    asks.close()
    bids.close()
   


def upload_orderbook():
    # Calculate timespan
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    end  = time.mktime(today.timetuple())
    start = end - (24 * 60 * 60)

    zip_dst = os.path.join(tmpdirname, f"{yesterday.strftime('%Y-%m-%d')}.zip")
    zip_files([orderbook_dst, asks_dst, bids_dst], zip_dst)
    logging.info(f"Zip files to {zip_dst}")
    upload_blob('coin-project-storage', zip_dst, f"orderbook/{os.path.basename(zip_dst)}")
    logging.info(f"Uploaded {zip_dst} to GCS")



if __name__ == "__main__":
    # Create an instance of the scheduler
    scheduler = BlockingScheduler()

    # Schedule the task to run at 5 minutes past midnight every day
    scheduler.add_job(upload_orderbook, 'cron', minute=5, hour=0)
    
    # Start the scheduler
    scheduler.start()
