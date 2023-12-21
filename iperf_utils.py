# from time import sleep

# def iperf_commands(index, h1, h2, port, cong, duration, outdir, delay=0):
#     # -c [ip]: remote host
#     # -w [size]: TCP buffer size
#     # -C: congestion control
#     # -t [seconds]: duration
#     # -p [port]: port
#     # -f m: format in megabits
#     # -i 1: measure every second
#     window = ''
#     client = "iperf3 -c {} -f m -i 1 -p {} {} -C {} -t {} > {}".format(
#         h2['IP'], port, window, cong, duration, "{}/iperf{}.txt".format(outdir, index)
#     )
#     h1['runner'](client, background=True)

# def iperf_setup(h1, h2, ports):
#     print("Killing all the iperf3 processes")
#     h2['runner']("killall iperf3")
#     print("Done")
#     sleep(1)  # make sure ports can be reused
#     for port in ports:
#         # -s: server
#         # -p [port]: port
#         # -f m: format in megabits
#         # -i 1: measure every second
#         # -1: one-off (one connection then exit)
#         cmd = "iperf3 -s -p {} -f m -i 1 -1".format(port)
#         h2['runner'](cmd, background=True)
#     sleep(min(10, len(ports)))  # make sure all the servers start

from time import sleep


def iperf_commands(index, host_1, host_2, target_port, cong, duration, outdir, delay=0):
    """
    Run an iperf client command on host h1 to connect to iperf server on host h2.

    Parameters:
    - index: Index of the flow.
    - h1: Source host.
    - h2: Destination host.
    - port: Port for the iperf server.
    - cong: Congestion control algorithm to use.
    - duration: Duration of the iperf experiment.
    - outdir: Output directory.
    - delay: Delay before starting the iperf experiment.
    """
    window = ""
    client_command = f"iperf3 -c {host_2['IP']} -f m -i 1 -p {target_port} {window} -C {cong} -t {duration} > {f'{outdir}/iperf{index}.txt'}"
    host_1["runner"](client_command, background=True)


def iperf_conf_setup(host_2, target_port):
    """
    Set up iperf servers on the destination host (h2) using specified ports.

    Parameters:
    - host_2: Destination host.
    - port: port for iperf server.
    """
    print("Terminating all iperf3 processes on Host 2")
    host_2["runner"]("killall iperf3")
    sleep(2)
    host_2["runner"](f"iperf3 -p {target_port}  -s  -f  m  -i  1  -1", background=True)
    sleep(2)
