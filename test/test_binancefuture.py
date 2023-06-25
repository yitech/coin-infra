import asyncio
from coin_infra.datapipe import BinanceFuturesOrderbook

async def stop_after_seconds(book, seconds):
    await asyncio.sleep(seconds)
    await book.stop()

async def main():
    bn = BinanceFuturesOrderbook("wss://fstream.binance.com/ws/btcusdt@depth5@100ms", "BTCUSDT")
    run = asyncio.create_task(bn.run())
    stop = asyncio.create_task(stop_after_seconds(bn, 10))

    await run
    await stop


if __name__ == "__main__":
    asyncio.run(main())
    