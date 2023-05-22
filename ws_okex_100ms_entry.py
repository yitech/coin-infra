import argparse
from source_collector import WebsocketOkexBridge

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='config.json', help='Path to configuration file')
    args = parser.parse_args()

    WebsocketOkexBridge.setup_logging()
    config = WebsocketOkexBridge.read_config_file(args.config)
    
    bridge = WebsocketOkexBridge(
        config['kafka_url'], 
        config['kafka_topic'], 
        config['partition'],
        config['exchange'],
        config['symbol'],
        config['websocket_url'],
        config['args']
        )
    bridge.run()

