#!/bin/bash

set -xe

# Validate command-line arguments
if [ $# -ne 2 ]; then
  echo "Usage: ./console.sh <python_script> <config_file>"
  exit 1
fi

# Get arguments
python_script=$1
config_file=$2

# Get the base name of the config file without extension
config_file_base=$(basename $config_file .json)

# Construct filenames
timestamp=$(date +"%Y%m%d%H%M%S")
log_file="/home/yite/coin-infra/artifact/log/${config_file_base}_${timestamp}.log"

# Set the Python executable path
python_exec="/home/yite/coin-infra/venv/bin/python"

# Execute the command
nohup $python_exec $python_script $config_file >> $log_file 2>&1 &