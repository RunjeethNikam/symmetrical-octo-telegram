#!/bin/bash
#
# run_experiments.sh
# 
# This script sources configurations from configurations.sh,
# runs experiments on a remote VM using gcloud compute ssh,
# and downloads the generated figures.

# Source project configurations
source configurations.sh

# Run experiments on the remote VM
echo "Executing experiments on $HOST_1"
gcloud compute ssh  --zone "$ZONE" --project "$GCLOUD_PROJECT" "$HOST_1" --command "cd ~/experiment && bash generate_figures.sh"

# Download generated figures from the remote VM
echo "Downloading the figures from $HOST_1"
gcloud compute scp --recurse --zone "$ZONE" --project "$GCLOUD_PROJECT" "$HOST_1:~/experiment/figures" ./

# Display completion message
echo "Experiments completed successfully."
