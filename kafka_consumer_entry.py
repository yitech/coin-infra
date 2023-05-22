import argparse
from consumer import KafkaConsumer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='config.json', help='Path to configuration file')
    args = parser.parse_args()

    KafkaConsumer.setup_logging()
    config = KafkaConsumer.read_config_file(args.config)
    
    bridge = KafkaConsumer(
        config["kafka_url"],
        config["group_id"],
        config["kafka_topic"],
        config["influx_url"],
        config["influx_token"],
        config["influx_org"],
        config["influx_bucket"]
        )
    bridge.run()