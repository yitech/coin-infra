from fastapi import FastAPI
import ccxt.async_support as ccxt

app = FastAPI()
exchange = ccxt.binance({
    'apiKey': 'aoh341Mu0rqR97KhZQvhHg5X2RaG1jmZiF45OW1sgXvxt3VcBvKaSfSkcZhPoqpe',
    'secret': 'JFoNNmkvvTNSVAndP6OvENnUWIpnPhLqn0y3bFRUxW5TF5goUusrMQIkORMSzK8v',
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
async def get_orderbook(symbol: str):
    return await exchange.fetch_order_book(symbol)


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
