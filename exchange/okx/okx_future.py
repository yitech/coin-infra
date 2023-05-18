import os
from fastapi import FastAPI
import ccxt.async_support as ccxt
import json

# Parse command-line arguments
config_path = os.environ.get('CONFIG_PATH')

# Read the configuration file
with open(config_path, 'r') as f:
    config = json.load(f)

app = FastAPI()
exchange = ccxt.okx({
    'apiKey': config['api_key'],
    'secret': config['api_secret'],
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})


@app.on_event("shutdown")
async def shutdown_event():
    await exchange.close()


@app.get("/ticker")
async def get_ticker(symbol: str):
    return await exchange.fetch_ticker(symbol)


@app.get("/orderbook")
async def get_orderbook(symbol: str, limit: int):
    return await exchange.fetch_order_book(symbol, limit)


@app.post("/open_position")
async def open_position(symbol: str, side: str, amount: float):
    market_order = {
        'symbol': symbol,
        'side': side,
        'type': 'market',
        'quantity': amount,
    }
    return await exchange.create_order(**market_order)


@app.post("/close_position")
async def close_position(symbol: str):
    position = await exchange.fetch_position(symbol)
    close_order = {
        'symbol': symbol,
        'side': 'buy' if position['side'] == 'sell' else 'sell',
        'type': 'market',
        'quantity': position['amount'],
    }
    return await exchange.create_order(**close_order)
