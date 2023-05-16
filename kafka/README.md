# Kafka Docker Setup

This project provides a Docker Compose setup for running a local Kafka instance along with Zookeeper and the Confluent Control Center.

## Prerequisites

You need to have Docker and Docker Compose installed on your machine. If you don't have them installed, you can download them from Docker's website.

## Services

The Docker Compose setup includes the following services:

* `zookeeper`: This is required for Kafka. It manages the Kafka brokers and keeps track of their status.
* `kafka`: This is the Kafka service where you can create topics and produce/consume messages.
* `control-center`: This is the Confluent Control Center that provides a web-based UI for managing and monitoring your Kafka environment.

## Running the Services

Navigate to the directory containing the `docker-compose.yml` file and run the following command to start the services:

```bash
docker compose up -d
```

You can access Kafka at localhost:9092 and the Confluent Control Center at http://localhost:9021.

## Stopping the Services
To stop the services, you can press Ctrl+C in the terminal where you ran docker-compose up. If you started the services in the background (using docker-compose up -d), you can stop them using the following command:
```bash
docker compose down
```

## Viewing Logs
You can view the logs of the services using the following command:
```bash
docker compose logs
```

To view the logs of a specific service, for example, kafka, you can use the following command:
```bash
docker compose logs kafka
```

## Adjusting Configuration
The provided configuration is suitable for local development and testing. For a production setup, you'll need to adjust the configuration parameters in the docker-compose.yml file and consider factors like data persistence, performance tuning, and security.

This README provides basic instructions for starting, stopping, and viewing the logs of the Docker Compose setup. It also provides a brief description of the services and a note about the configuration. You might need to adjust the instructions and descriptions to match your specific setup and requirements.

