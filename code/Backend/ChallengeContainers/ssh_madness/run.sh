#!/bin/bash
pushd /usr/local/share 
# Generate Users
./generate_ssh_users.sh
# Remove script evidence
rm -r *
popd

# Now run the ssh server
cd /home
service ssh start

# Function to handle SIGINT signal
sigint_handler() {
    echo "Received SIGINT signal. Stopping SSH service..."
    # Stop SSH service
    service ssh stop
    exit 0
}

# Trap SIGINT signal and call sigint_handler function
trap sigint_handler SIGINT

# Wait indefinitely with a sleep command
echo "SSH service started. Waiting for SIGINT signal..."
while true; do
    sleep 3600  # Sleep for an hour before checking for signals again
done

