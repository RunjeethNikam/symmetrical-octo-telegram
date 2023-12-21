from subprocess import Popen
from multiprocessing import Process

DEFAULT_DIR = "."


def capture_packets(options="", filename=f"{DEFAULT_DIR}/capture.dmp", runner=None):
    """
    Capture packets using tcpdump.

    Parameters:
    - options: Additional options for tcpdump command.
    - filename: Name of the output file for captured packets.
    - runner: Function to run the tcpdump command.

    Returns:
    - Return code of the tcpdump process.
    """
    command = f"tcpdump -Z root -w {filename} {options}; chmod +xwr {filename}"
    print(command)
    runner = Popen if runner is None else runner
    return runner(command, shell=True).wait()


def start_capture(output_file="capture.dmp"):
    """
    Start capturing packets in a separate process.

    Parameters:
    - output_file: Name of the output file for captured packets.

    Returns:
    - Process object for the packet capture.
    """
    monitor = Process(target=capture_packets, args=("", output_file))
    monitor.start()
    return monitor


def filter_capture(filter_expression, input_file="capture.dmp", output_file="filtered.dmp"):
    """
    Filter captured packets using tcpdump in a separate process.

    Parameters:
    - filter_expression: Expression to filter packets.
    - input_file: Input file containing captured packets.
    - output_file: Name of the output file for filtered packets.

    Returns:
    - Process object for the packet filtering.
    """
    monitor = Process(
        target=capture_packets, args=(f"-r ./{input_file} {filter_expression}", output_file)
    )
    monitor.start()
    return monitor
