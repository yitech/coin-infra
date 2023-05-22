import argparse
from source_collector.ws_bridge import WebsocketKafkaBridge

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='config.json', help='Path to configuration file')
    args = parser.parse_args()

    WebsocketKafkaBridge.setup_logging()
    config = WebsocketKafkaBridge.read_config_file(args.config)
    
    bridge = WebsocketKafkaBridge(
        config['kafka_url'], 
        config['kafka_topic'], 
        config['partition'],
        config['symbol'],
        config['websocket_url']
        )
    bridge.run()

