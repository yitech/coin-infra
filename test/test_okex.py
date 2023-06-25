import asyncio
from coin_infra.datapipe import OkexOrderbook

async def stop_after_seconds(book, seconds):
    await asyncio.sleep(seconds)
    await book.stop({
        "op": "unsubscribe",
        "args": [{
            "channel": "books5",
            "instId": "BTC-USDT-SWAP"
        }]
    })

async def main():
    okx = OkexOrderbook("wss://ws.okx.com:8443/ws/v5/public", "BTCUSDT")
    run = asyncio.create_task(okx.run({
        "op": "subscribe",
        "args": [{
            "channel": "books5",
            "instId": "BTC-USDT-SWAP"
        }]
    }))
    stop = asyncio.create_task(stop_after_seconds(okx, 10))

    await run
    await stop


if __name__ == "__main__":
    asyncio.run(main())
