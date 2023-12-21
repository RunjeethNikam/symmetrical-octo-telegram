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

    def start_flows(
        nw,
        number_of_flows,
        time_between_flows,
        flow_type,
        cc,
        pre_experiment_action=None,
        experiment_monitor=None,
    ):
        """
        Start multiple flows for the network experiment.

        Parameters:
        - net: Network configuration.
        - num_flows: Number of flows to start.
        - time_btwn_flows: Time between starting each flow.
        - flow_type: Type of flow (e.g., 'iperf').
        - cong: List of congestion control algorithms for each flow.
        - pre_flow_action: Pre-flow action to perform.
        - flow_monitor: Flow monitoring function.

        Returns:
        - List of flow configurations.
        """
        host_1 = nw["h1"]
        host_2 = nw["h2"]

        flows = []
        basic_port = 1234

        print("Setting up the Iperf configuration")
        iperf_conf_setup(host_2, basic_port)
        flow_commands = iperf_commands

        def start_experiment(i):
            pre_experiment_action(nw, i, basic_port + i)
            flow_commands(
                i,
                host_1,
                host_2,
                basic_port + i,
                cc[i],
                args.time - time_between_flows * i,
                args.dir,
                delay=i * time_between_flows,
            )
            flow = {
                "index": i,
                "send_filter": "src {} and dst {} and dst port {}".format(
                    host_1["IP"], host_2["IP"], basic_port + i
                ),
                "receive_filter": "src {} and dst {} and src port {}".format(
                    host_2["IP"], host_1["IP"], basic_port + i
                ),
                "monitor": None,
            }
            flow["filter"] = '"({}) or ({})"'.format(
                flow["send_filter"], flow["receive_filter"]
            )
            if experiment_monitor:
                print(
                    "########################### Found A Monitor ###########################"
                )
                flow["monitor"] = experiment_monitor(nw, i, basic_port + i)
            else:
                print(
                    "########################### Not Found ###########################"
                )
            flows.append(flow)

        s = sched.scheduler(time, sleep)
        for i in range(number_of_flows):
            s.enter(i * time_between_flows, 1, start_experiment, (i,))
        s.run()
        return flows

    def run(action):
        """
        Execute the specified action.

        Parameters:
        - action: Function representing the action to be performed.
        """
        if not os.path.exists(args.dir):
            os.makedirs(args.dir)

        net = build_topology(args)
        action(net)

    def figure5(net):
        """Run the Figure 5 experiment."""

        def pinger(name):
            """
            Start a ping train between two hosts for a specified duration.

            Parameters:
            - name: Name of the ping configuration.
            """

            def ping_fn(net, i, port):
                start_ping(net, args.time, "{}_rtt.txt".format(name), args)

            return ping_fn

        cap = start_capture("{}/capture_bbr.dmp".format(args.dir))

        flows = start_flows(
            net, 1, 0, args.flow_type, ["bbr"], pre_experiment_action=pinger("bbr")
        )
        display_countdown(args.time + 5)

        Popen("killall tcpdump", shell=True)
        cap.join()
        filter_capture(
            flows[0]["filter"],
            "{}/capture_bbr.dmp".format(args.dir),
            "{}/flow_bbr.dmp".format(args.dir),
        )
        cap = start_capture("{}/capture_cubic.dmp".format(args.dir))

        flows = start_flows(
            net, 1, 0, args.flow_type, ["cubic"], pre_experiment_action=pinger("cubic")
        )
        display_countdown(args.time + 5)

        Popen("killall tcpdump", shell=True)
        cap.join()
        filter_capture(
            flows[0]["filter"],
            "{}/capture_cubic.dmp".format(args.dir),
            "{}/flow_cubic.dmp".format(args.dir),
        )

    run(figure5)


# Example usage:
# run_experiment(command_line_arguments)
