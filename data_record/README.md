# Pushing data into influxDB

The script is consuming data from kafka and insert to influxDB

## Running the service

The service can be run locally using Python, or using Docker.

### Running with Docker
```bash
docker build -t data_recorder .
```

```bash
docker run --rm -v path/to/config.json:/app/config.json -e CONFIG_PATH=/app/config.json --network=coin-network data_recorder
```

- -v should be "$(pwd)"/config.json:/app/config.json
