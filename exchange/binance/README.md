# FastAPI with CCXT for Binance Futures

This is a simple FastAPI application that uses the `ccxt` library to interact with Binance Futures. It provides endpoints to fetch ticker information, fetch the order book, and to open and close positions.

## Requirements

- Docker

## Getting Started

1 Build the Docker image:

```bash
docker build -t binance-app .
```

2 Run the Docker container:

```bash
docker run -it --rm --name=binancefuture -v path/to/config.json:/app/config.json -e CONFIG_PATH=/app/config.json -p 40000:40000 --network=coin-network binance-app
```

- -v should be "$(pwd)"/config_btc_usdt_perp.json:/app/config.json

The application is now running at `http://localhost:40000`.

## API Endpoints

The following endpoints are available:

- `GET /ticker?symbol=<symbol>`: Fetches the ticker for the specified symbol.
- `GET /orderbook?symbol=<symbol>`: Fetches the order book for the specified symbol.
- `POST /open_position`: Opens a position with a market order. The request body should be a JSON object with `symbol`, `side` ('buy' or 'sell'), and `amount` (the amount to buy or sell).
- `POST /close_position`: Closes a position with a market order. The request body should be a JSON object with the `symbol`.

## Note

This is a basic example and lacks error handling. In a production setting, you should add proper error handling to ensure that the server behaves correctly when API calls fail.
