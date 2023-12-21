from time import sleep

def run_iperf_client(index, source_host, destination_host, target_port, congestion, duration, output_dir, delay=0):
    """
    Run an iperf client command on the source host to connect to the iperf server on the destination host.

    Parameters:
    - index: Index of the flow.
    - source_host: Source host.
    - destination_host: Destination host.
    - target_port: Port for the iperf server.
    - congestion: Congestion control algorithm to use.
    - duration: Duration of the iperf experiment.
    - output_dir: Output directory.
    - delay: Delay before starting the iperf experiment.
    """
    window = ""
    client_command = f"iperf3 -c {destination_host['IP']} -f m -i 1 -p {target_port} {window} -C {congestion} -t {duration} > {output_dir}/iperf{index}.txt"
    source_host["runner"](client_command, background=True)


def setup_iperf_servers(destination_host, target_port):
    """
    Set up iperf servers on the destination host using the specified port.

    Parameters:
    - destination_host: Destination host.
    - target_port: Port for the iperf server.
    """
    print("Terminating all iperf3 processes on Destination Host")
    destination_host["runner"]("killall iperf3")
    sleep(2)
    destination_host["runner"](f"iperf3 -p {target_port} -s -f m -i 1 -1", background=True)
    sleep(2)
