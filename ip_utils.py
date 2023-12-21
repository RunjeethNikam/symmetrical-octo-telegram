import socket


def get_ip_address(test_destination):
    """
    Get the IP address of the local machine.

    Parameters:
    - test_destination: A destination used to determine the local IP address.

    Returns:
    - The local IP address.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((test_destination, 80))
    return s.getsockname()[0]


def start_ping(nw, time, fname, args):
    """
    Start a ping train between two hosts for a specified duration.

    Parameters:
    - net: Network configuration.
    - time: Duration of the ping train in seconds.
    - fname: Output filename for ping results.
    """
    h1 = nw["h1"]
    h2 = nw["h2"]

    # Command to initiate ping
    h1["runner"](
        f"ping -i 0.1 -c {int(time * 10)} {h2['IP']} > {args.dir}/{fname}",
        background=True,
    )


# Example usage:
# start_ping(network_configuration, 60, "ping_results.txt")
