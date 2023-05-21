# Bitcoin Ticker Listener Service

This service listens to Bitcoin ticker information from two endpoints and publishes it to a Kafka topic. The service is implemented using Python's FastAPI and aiohttp for async requests, and Confluent's Kafka Python client for interacting with Kafka.

## Running the service

The service can be run locally using Python, or using Docker.

### Running with Docker
```bash
docker build -t data-source .
```

```bash
docker run --rm --name <source-name> -v path/to/config.json:/app/config.json -e CONFIG_PATH=/app/config.json --network=coin-network data-source
```

- -v should be "$(pwd)"/config_binance_btc_usdt_perp.json:/app/config.json

### Production command
```bash
docker run --rm --name btc-source -v "$(pwd)"/config_binance_btc_usdt_perp.json:/app/config.json -e CONFIG_PATH=/app/config.json --network=coin-network data-source
```




