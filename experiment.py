import os
from subprocess import Popen
from time import sleep, time
import sched

from monitor import start_capture, filter_capture
from iperf_utils import iperf_commands, iperf_conf_setup
from timer_utils import display_countdown
from ip_utils import start_ping
from utils import build_topology


def run_experiment(args):
    """
    Run a network experiment using iperf, retrieve the destination IP address,
    gather metrics, sanitize the data, and plot the results.

    Parameters:
    - args: Command-line arguments specifying experiment parameters.
    """

    def setup_iperf_flows(
        network,
        num_flows,
        time_between_flows,
        flow_type,
        congestion_controls,
        pre_experiment_action=None,
        experiment_monitor=None,
    ):
        """
        Set up and start multiple flows for the network experiment using iperf.

        Parameters:
        - network: Network configuration.
        - num_flows: Number of flows to start.
        - time_between_flows: Time between starting each flow.
        - flow_type: Type of flow (e.g., 'iperf').
        - congestion_controls: List of congestion control algorithms for each flow.
        - pre_experiment_action: Pre-flow action to perform.
        - experiment_monitor: Flow monitoring function.

        Returns:
        - List of flow configurations.
        """
        source_host = network["host_1"]
        destination_host = network["host_2"]

        flows = []
        base_port = 9999

        print("Setting up the Iperf configuration")
        iperf_conf_setup(destination_host, base_port)
        flow_commands = iperf_commands

        def start_single_flow(i):
            pre_experiment_action(network, i, base_port + i)
            flow_commands(
                i,
                source_host,
                destination_host,
                base_port + i,
                congestion_controls[i],
                args.time - time_between_flows * i,
                args.dir,
                delay=i * time_between_flows,
            )
            flow = {
                "index": i,
                "send_filter": f"dst port {base_port + i} and dst {destination_host['IP']} and src {source_host['IP']}",
                "receive_filter": f"src port {base_port + i} and src {destination_host['IP']} and dst {source_host['IP']}",
                "monitor": None,
            }
            flow["filter"] = f'"{flow["send_filter"]} or {flow["receive_filter"]}"'
            if experiment_monitor:
                print("########################### Found A Monitor ###########################")
                flow["monitor"] = experiment_monitor(network, i, base_port + i)
            else:
                print("########################### Not Found ###########################")
            flows.append(flow)
        sdl = sched.scheduler(time, sleep)
        
        for index in range(num_flows):
            sdl.enter(index * time_between_flows, 1, start_single_flow, (index,))
        sdl.run()
        return flows

    def run_network_action(action_fn):
        """
        Execute the specified action function on the network.

        Parameters:
        - action_fn: Function representing the action to be performed.
        """
        if not os.path.exists(args.dir):
            os.makedirs(args.dir)

        network_config = build_topology(args)
        action_fn(network_config)

    def figure5_experiment(network):
        """Run the Figure 5 experiment."""

        def configure_pinger(name):
            """
            Configure and return a ping function between two hosts for a specified duration.

            Parameters:
            - name: Name of the ping configuration.
            """

            def ping_function(net, i, port):
                start_ping(net, args.time, f"{name}_rtt.txt", args)

            return ping_function

        capture_bbr = start_capture(f"{args.dir}/bbr-packets.dmp")

        flows_bbr = setup_iperf_flows(
            network,
            1,
            0,
            args.flow_type,
            ["bbr"],
            pre_experiment_action=configure_pinger("bbr"),
        )
        display_countdown(args.time + 5)

        Popen("killall tcpdump", shell=True)
        capture_bbr.join()
        filter_capture(
            flows_bbr[0]["filter"],
            f"{args.dir}/bbr-packets.dmp",
            f"{args.dir}/sanitized-bbr.dmp",
        )

        capture_cubic = start_capture(f"{args.dir}/cubic-packets.dmp")

        flows_cubic = setup_iperf_flows(
            network,
            1,
            0,
            args.flow_type,
            ["cubic"],
            pre_experiment_action=configure_pinger("cubic"),
        )
        display_countdown(args.time + 5)

        Popen("killall tcpdump", shell=True)
        capture_cubic.join()
        filter_capture(
            flows_cubic[0]["filter"],
            f"{args.dir}/cubic-packets.dmp",
            f"{args.dir}/sanitized-cubic.dmp",
        )

    run_network_action(figure5_experiment)


# Example usage:
# run_experiment(command_line_arguments)
