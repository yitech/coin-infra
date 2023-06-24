import asyncio
from coin_infra.datapipe import BinanceFuturesOrderbook


if __name__ == "__main__":
    bn = BinanceFuturesOrderbook("wss://fstream.binance.com/ws/btcusdt@depth5@100ms", "BTCUSDT")
    asyncio.run(bn.run())