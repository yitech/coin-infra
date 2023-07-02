#!/bin/bash

set -xe

workspace="/home/yite/coin-infra"
export PYTHONPATH=$workspace

# Construct filenames
timestamp=$(date +"%Y%m%d%H%M%S")
log_file="${workspace}/artifact/log/${timestamp}.log"

# Set the Python executable path
python_exec="/home/yite/coin-infra/venv/bin/python"

# Execute agent
nohup $python_exec "${workspace}/agent/binance_publisher.py" "${workspace}/configuration/config_binancefutures_btc_usdt.json" >> $log_file 2>&1 &
# Execute subscriber
nohup $python_exec "${workspace}/agent/subscriptor.py" "${workspace}/configuration/config_binancefutures_btc_usdt.json" >> $log_file 2>&1 &