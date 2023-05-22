import json
import time
import websocket
from threading import Thread

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, code, reason):
    print(f"### closed: {code} {reason} ###")

def on_open(ws):
    def run(*args):
        while True:
            # This is the request to get the orderbook with depth 5
            data = {
                "op": "subscribe",
                "args": [
                    {
                        "channel": "books5",
                        "instId": "BTC-USDT-SWAP"
                    }
                ]
            }
            ws.send(json.dumps(data))
            time.sleep(0.1)  # sleep for 100ms
    Thread(target=run).start()

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://ws.okx.com:8443/ws/v5/public",
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
