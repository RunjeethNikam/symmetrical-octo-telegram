#!/bin/bash
#
# run_experiment.sh
# 
# This script performs a network experiment using iperf, retrieves the destination IP address,
# gathers metrics, sanitizes the data, and plots the results.

# Function to run the network experiment
run_experiment() {
    type=$1          # Type of the flow (e.g., iperf)
    dir=$2           # Directory to store experiment outputs
    oldpwd=$PWD

    # Create the figures directory
    echo "Creating the figures directory"
    mkdir -p "$dir"

    # Clean the previous data
    echo "Clean the previous data"
    rm -rf "$dir"/*

    flow=1
    maxq=150

    echo "Running $type experiment..."

    # Retrieve the destination IP address
    echo "Retrieving the Destination IP address"
    destip=$(su $SUDO_USER -c "cat ~/.bbr_pair_ip")
    echo "Done"

    # Install Python dependencies
    echo "Installing Python dependencies"
    pip3 install -r requirements.txt
    echo "Done"

    # Run the network experiment and gather metrics
    echo "Getting the metrics"
    python3 main.py --time 20 --dest-ip "$destip" --bw-net 10 --delay 35 --maxq "$maxq" --environment vms --flow-type "$type" --dir "$dir"
    chmod -R 0777 "$dir"
    echo "Done"

    # Sanitize the data using tshark
    echo "Sanitizing the data"
    su $SUDO_USER -c "tshark -2 -r $dir/flow_bbr.dmp -R 'tcp.stream eq $flow && tcp.analysis.ack_rtt' -e frame.time_relative -e tcp.analysis.ack_rtt -Tfields -E separator=, > $dir/bbr_rtt.txt"
    su $SUDO_USER -c "tshark -2 -r $dir/flow_cubic.dmp -R 'tcp.stream eq $flow && tcp.analysis.ack_rtt' -e frame.time_relative -e tcp.analysis.ack_rtt -Tfields -E separator=, > $dir/cubic_rtt.txt"
    echo "Done"

    # Plot the results
    echo "Plotting the results"
    python3 plot_ping.py -f "$dir/bbr_rtt.txt" "$dir/cubic_rtt.txt" --xlimit 35 -o "$dir/figure5_$type.png"
    echo "Done"
}

# Example usage:
run_experiment "iperf" "figure5_iperf"
