import csv
import json
import os
import logging
from datetime import datetime, timezone, timedelta
import glob
import zipfile

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

SOURCE_DIR = '/home/yite/coin-datapipe/artifact/data'
OUT_DIR = '/home/yite/coin-datapipe/artifact/dataframe'

def convert_to_orderbook(date):
    orderbook = open(os.path.join(OUT_DIR, 'orderbook.csv'), 'w')
    orderbook_writer = csv.writer(orderbook)
    asks = open(os.path.join(OUT_DIR, 'asks.csv'), 'w')
    orderbook_writer.writerow(['id', 'timestamp', 'symbol', 'exchange'])
    asks_writer = csv.writer(asks)
    asks_writer.writerow(['id', 'price', 'size'])
    bids = open(os.path.join(OUT_DIR, 'bids.csv'), 'w')
    bids_writer = csv.writer(bids)
    bids_writer.writerow(['id', 'price', 'size'])
    for root, dirs, files in os.walk(SOURCE_DIR):
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
                        for price, size in data['ask']:
                            asks_writer.writerow([data['id'], price, size])
                        # for price, size in data['bid']:  
                        for row in data['bid']: # only valid when 6/6
                            bids_writer.writerow([data['id'], row[0], row[1]])
                    line = log.readline()
    orderbook.close()
    asks.close()
    bids.close()

def clear_raw(date):
    # Format the date as 'YYYYMMDD'
    date_str = date.strftime("%Y%m%d")
    # Construct the file pattern
    file_pattern = os.path.join(SOURCE_DIR, f"*{date_str}*")

    # Get a list of all files that match the pattern
    files = sorted(glob.glob(file_pattern))

    # Remove each file
    for file in files:
        try:
            # os.remove(file)
            logging.info(f"File {file} has been removed successfully")
        except:
            logging.error(f"Error while deleting file : {file}")


def zip_orderbook(date):
    # Format the date as 'yyyy-mm-dd'
    date_str = date.strftime("%Y-%m-%d")

    # Define the name of the zip file
    zip_file_name = os.path.join(OUT_DIR, f"{date_str}.zip")

    # Create the zip file (in write mode)
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        # Loop over all the files in the directory
        for root, dirs, files in os.walk(OUT_DIR):
            for file in files:
                # Construct the file's full path
                file_path = os.path.join(root, file)
                # Add the file to the zip file
                if file_path != zip_file_name:
                    zipf.write(file_path, arcname=os.path.basename(file_path))
                    logging.info(f"File {file_path} has been added to zip")
    logging.info(f"All files zipped successfully into {zip_file_name}")

def clear_csv():
    # Construct the file pattern
    file_pattern = os.path.join(OUT_DIR, "*.csv")
    # Get a list of all files that match the pattern
    files = sorted(glob.glob(file_pattern))
    # Remove each file
    for file in files:
        try:
            # os.remove(file)
            logging.info(f"File {file} has been removed successfully")
        except:
            logging.error(f"Error while deleting file : {file}")





if __name__ == "__main__":
    # Get today's date
    today = datetime.now(timezone.utc)
    # Subtract one day to get yesterday's date
    yesterday = today - timedelta(days=1)
    # Use date part only for comparison in the function
    date = yesterday.date()
    # convert raw data to orderbook data
    convert_to_orderbook(date)
    # clear raw data
    clear_raw(date)
    # zipfile
    zip_orderbook(date)
    # clear csv
    clear_csv()