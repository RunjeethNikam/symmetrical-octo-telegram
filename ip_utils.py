import socket
import subprocess

def get_local_ip_address(test_destination, port=80):
    """
    Get the local machine's IP address.

    Parameters:
    - test_destination: A destination used to determine the local IP address (default is Google's public DNS).
    - port: Port number for the test destination (default is 80).

    Returns:
    - The local IP address.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((test_destination, port))
        return s.getsockname()[0]

def start_ping(host1, host2, duration=60, output_filename="ping_results.txt", directory="."):
    """
    Start a ping train between two hosts for a specified duration.

    Parameters:
    - host1: IP address or hostname of the first host.
    - host2: IP address or hostname of the second host.
    - duration: Duration of the ping train in seconds (default is 60).
    - output_filename: Output filename for ping results (default is "ping_results.txt").
    - directory: Output directory for the ping results file (default is the current directory).
    """
    ping_command = f"ping -i 0.1 -c {int(duration * 10)} {host2}"

    output_path = f"{directory}/{output_filename}"

    # Use subprocess to run the ping command in the background
    subprocess.run(ping_command, shell=True, stdout=open(output_path, "w"))

# Example usage:
# local_ip = get_local_ip_address()
# network_config = {"h1": {"IP": local_ip}, "h2": {"IP": "192.168.1.2"}}
# start_ping(network_config["h1"]["IP"], network_config["h2"]["IP"])
