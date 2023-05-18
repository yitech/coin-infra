# Bitcoin Ticker Listener Service

This service listens to Bitcoin ticker information from two endpoints and publishes it to a Kafka topic. The service is implemented using Python's FastAPI and aiohttp for async requests, and Confluent's Kafka Python client for interacting with Kafka.

## Running the service

The service can be run locally using Python, or using Docker.

### Running with Docker
```bash
docker build -t data_source .
```

```bash
docker run --rm -p 39000:39000 --network=coin-network data_source
```



