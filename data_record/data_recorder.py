from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import time
import influxdb_client

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS

app = FastAPI()

# setup connection
token = "4tHRvseKoN8TfRm0pNmGoJIiDnblMEzJlM-XpYLXbm5e_LgtPipx38rXmZphsTNasFJ2o148ji-amFu3d6t7YA=="
org = "Dev Team"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"


class InfluxRecorder:
    def __init__(self, token, org, url):
        self.client = InfluxDBClient(url=url, token=token)
        self.org = org
        self.write_api = self.client.write_api(write_options=ASYNCHRONOUS)

    def insert(self, bucket, payload):
        data_price = Point("stock_price").field("price", payload.price).time(payload.timestamp, WritePrecision.NS)
        data_ask = [Point("orderbook_ask").field("ask_price", price).field("ask_size", size).time(payload.timestamp, WritePrecision.NS) for price, size in payload.orderbook["ask"]]
        data_bid = [Point("orderbook_bid").field("bid_price", price).field("bid_size", size).time(payload.timestamp, WritePrecision.NS) for price, size in payload.orderbook["bid"]]
        self.write_api.write(bucket, self.org, data_price + data_ask + data_bid)

    def close(self):
        self.client.close()

app = FastAPI()

class StockData(BaseModel):
    timestamp: int
    price: float
    orderbook: dict

recorder = InfluxRecorder(token=token, org=org, url=url)

@app.post("/insert")
async def insert_stock_data(bucket: str, data: StockData):
    recorder.insert(bucket, data)
    return {"message": "Data inserted successfully"}

@app.on_event("shutdown")
def shutdown_event():
    recorder.close()
