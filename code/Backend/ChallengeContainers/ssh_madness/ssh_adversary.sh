#!/bin/bash

echo "Creating Background Process to Disable Competitor"

# Start the daemon
nohup "$(dirname $0)/runner.sh" > /dev/null 2>&1 &

sleep 10

echo "Timebomb is Away"
