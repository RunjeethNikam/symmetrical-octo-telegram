#!/bin/bash
# 
# This script generates and organizes figures related to the experiment.

# Create a directory to store figures
mkdir -p ./figures

# Run the figure5.sh script with the 'iperf' argument
sudo ./figure5.sh

# Copy the generated image to the main figures directory
cp ./figure5_iperf/figure5_iperf.png ./figures/figure5_iperf_vms.png

# Display a completion message
echo "Figures generated and organized successfully in the ./figures directory."
