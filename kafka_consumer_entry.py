import argparse
from consumer import KafkaToFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='config.json', help='Path to configuration file')
    args = parser.parse_args()

    KafkaToFile.setup_logging()
    config = KafkaToFile.read_config_file(args.config)
    
    bridge = KafkaToFile(
        config["kafka_url"],
        config["group_id"],
        config["kafka_topic"],
        config["file_storage"],
        config["batch_size"]
        )
    bridge.run()