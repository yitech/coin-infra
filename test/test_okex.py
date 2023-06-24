import asyncio
from coin_infra.datapipe import OkexOrderbook


if __name__ == "__main__":
    okx = OkexOrderbook("wss://ws.okx.com:8443/ws/v5/public", "BTCUSDT")
    asyncio.run(okx.run({
        "op": "subscribe",
        "args": [{
            "channel": "books5",
            "instId": "BTC-USDT-SWAP"
        }]
    }))