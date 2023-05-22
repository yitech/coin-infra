from flightsql import FlightSQLClient
import os
import logging
import time
import datetime
import zipfile
import tempfile
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

def sql_query_to_df(client, query):
    # Execute the query
    info = client.execute(query)
    reader = client.do_get(info.endpoints[0].ticket)

    # Convert to dataframe
    data = reader.read_all()
    df = data.to_pandas()
    return df

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


   


def upload_orderbook():
    # Calculate timespan
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    start  = time.mktime(today.timetuple())
    end = start + (24 * 60 * 60)

    query_client = FlightSQLClient(
                    host = "us-east-1-1.aws.cloud2.influxdata.com",
                    token = "4tHRvseKoN8TfRm0pNmGoJIiDnblMEzJlM-XpYLXbm5e_LgtPipx38rXmZphsTNasFJ2o148ji-amFu3d6t7YA==",
                    metadata={"bucket-name": "coin-project"}
                    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        logging.info(f'Created temporary directory {tmpdirname}')
        # Create a temporary directory to store the CSV files
        query = f"""SELECT * 
                    FROM orderbook 
                    WHERE timestamp BETWEEN {start} and {end}
                    ORDER BY timestamp DESC"""

        orderbook_df = sql_query_to_df(query_client, query)
        orderbook_dst = os.path.join(tmpdirname, "orderbook.csv")
        orderbook_df.to_csv(orderbook_dst, index=False)
        
        query = f"""SELECT asks.*
                    FROM asks
                    JOIN (
                        SELECT id
                        FROM orderbook
                        WHERE timestamp BETWEEN {start} and {end}
                    ) AS orderbook_filtered
                    ON asks.id = orderbook_filtered.id;
                """
        asks_df = sql_query_to_df(query_client, query)
        logging.info(f'Querying asks')
        asks_dst = os.path.join(tmpdirname, "asks.csv")
        logging.info(f'Queried asks to {asks_dst}')
        asks_df.to_csv(asks_dst, index=False)

        query = f"""SELECT bids.*
                    FROM bids
                    JOIN (
                        SELECT id
                        FROM orderbook
                        WHERE timestamp BETWEEN {start} and {end}
                    ) AS orderbook_filtered
                    ON bids.id = orderbook_filtered.id;
                """
        bids_df = sql_query_to_df(query_client, query)
        logging.info(f'Querying bids')
        bids_dst = os.path.join(tmpdirname, "bids.csv")
        bids_df.to_csv(bids_dst, index=False)
        logging.info(f'Queried bids to {bids_dst}')

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
