#!/bin/bash

set -xe

# Validate command-line arguments
if [ $# -ne 3 ]; then
  echo "Usage: ./run.sh <exchange> <symbol> <type>"
  exit 1
fi

# Assign arguments to variables
exchange=$1
symbol=$2
type=$3

# Construct filenames
log_file="${exchange}_${symbol}_${type}.log"
config_file="configuration/config_${exchange}_${symbol}_${type}.json"
python_script="ws_${exchange}_100ms_entry.py"

# Set the Python executable path
python_exec="$pwd/venv/bin/python"

# Execute the command
nohup $python_exec $python_script --config $config_file >> $log_file 2>&1 &
