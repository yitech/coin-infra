import argparse
from source_collector import WebsocketBinancefutureBridge

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='config.json', help='Path to configuration file')
    args = parser.parse_args()

    WebsocketBinancefutureBridge.setup_logging()
    config = WebsocketBinancefutureBridge.read_config_file(args.config)
    
    bridge = WebsocketBinancefutureBridge(
        config['kafka_url'], 
        config['kafka_topic'], 
        config['partition'],
        config['exchange'],
        config['symbol'],
        config['websocket_url']
        )
    bridge.run()

