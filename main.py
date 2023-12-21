#!/usr/bin/python
"""
BBR Replication Experiment Script

This script runs the BBR Replication experiment with the specified parameters.

Usage:
    python script.py --bw-net <bandwidth> --delay <delay> --dir <output_directory>
                    [--time <duration>] [--maxq <max_queue_size>] [--cong <congestion_algorithm>]
                    [--flow-type <flow_type>] [--environment <environment>] [--dest-ip <destination_ip>]

Parameters:
    --bw-net, -b: Bandwidth of the bottleneck (network) link in Mbps (required).
    --delay: Link propagation delay in milliseconds (required).
    --dir, -d: Directory to store experiment outputs (required).
    --time, -t: Duration in seconds to run the experiment (default: 10).
    --maxq: Maximum buffer size of the network interface in packets (default: 100).
    --flow-type: Type of flow (default: "iperf").
    --environment: Environment setting (default: "vms").
    --dest-ip: Destination IP address (default: "10.138.0.3").

Example:
    python script.py --bw-net 10 --delay 35 --dir /path/to/output --time 20
"""
from argparse import ArgumentParser

from experiment import run_experiment

parser = ArgumentParser(description="BBR Experiment Script")

parser.add_argument(
    "--bw-net",
    "-b",
    type=float,
    help="Bandwidth of the bottleneck (network) link in megabits per second (Mb/s)",
    required=True,
)
parser.add_argument(
    "--delay",
    type=float,
    help="Link propagation delay in milliseconds (ms)",
    required=True,
)
parser.add_argument(
    "--dir", "-d", help="Directory to store experiment outputs", required=True
)
parser.add_argument(
    "--time",
    "-t",
    help="Duration in seconds to run the experiment (default: 10 seconds)",
    type=int,
    default=10,
)
parser.add_argument(
    "--maxq",
    type=int,
    help="Maximum buffer size of the network interface in packets (optional)",
)
parser.add_argument("--flow-type", help="Type of flow for the experiment (optional)")
parser.add_argument(
    "--environment", help="Environment setting for the experiment (optional)"
)
parser.add_argument(
    "--dest-ip", help="Destination IP address for the experiment (optional)"
)


if __name__ == "__main__":
    args = parser.parse_args()
    run_experiment(args)
