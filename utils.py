import os
import json
from subprocess import Popen
from multiprocessing import Process

from ip_utils import get_ip_address, start_ping


def build_topology(args):
    def runner(popen, noproc=False):
        def run_fn(command, background=False, daemon=True):
            if noproc:
                p = popen(command, shell=True)
                if not background:
                    return p.wait()

            def start_command():
                popen(command, shell=True).wait()

            proc = Process(target=start_command)
            proc.daemon = daemon
            proc.start()
            if not background:
                proc.join()
            return proc

        return run_fn

    def ssh_popen(command, *args, **kwargs):
        user = os.environ.get("SUDO_USER", os.environ["USER"])
        full_command = "ssh -o StrictHostKeyChecking=no -i /home/{}/.ssh/id_rsa {}@{} '{} {}'".format(
            user, user, data["h2"]["IP"], "sudo bash -c", json.dumps(command)
        )
        kwargs["shell"] = True
        return Popen(full_command, *args, **kwargs)

    data = {
        "type": "emulator",
        "h1": {
            # IP address of this host
            "IP": get_ip_address(args.dest_ip),  # local IP address
            "popen": Popen,
        },
        "h2": {
            # IP address of H2 host
            "IP": args.dest_ip,
            "popen": ssh_popen,
        },
        "obj": None,
    }

    # set up tc qdiscs on hosts
    h2run = runner(data["h2"]["popen"], noproc=False)
    h1run = runner(data["h1"]["popen"], noproc=False)
    pipe_filter = (
        # delete the root queuing discipline
        "tc qdisc del dev {iface} root; "
        "tc qdisc add dev {iface} root handle 1: htb default 10; "
        "tc class add dev {iface} parent 1: classid 1:10 htb rate {rate}Mbit; "
        "tc qdisc add dev {iface} parent 1:10 handle 20: netem delay {delay}ms limit {queue}; "
    )
    ingress_filter = (
        "modprobe ifb numifbs=1; "
        "ip link set dev ifb0 up; "
        "ifconfig ifb0 txqueuelen 1000; "
        "tc qdisc del dev {iface} ingress; "
        "tc qdisc add dev {iface} handle ffff: ingress; "
        "tc filter add dev {iface} parent ffff: protocol all u32 match u32 0 0 action"
        " mirred egress redirect dev ifb0; "
    )
    pipe_args = {"rate": args.bw_net, "delay": args.delay, "queue": args.maxq}
    h2run(
        ingress_filter.format(iface="ens4")
        + pipe_filter.format(iface="ifb0", **pipe_args)
        + pipe_filter.format(iface="ens4", **pipe_args)
        + "sudo ethtool -K ens4 gso off tso off gro off; "
        "sudo ethtool -K ifb0 gso off tso off gro off; "
    )
    h1run(
        "tc qdisc del dev ens4 root; "
        "tc qdisc add dev ens4 root fq pacing; "
        "sudo ethtool -K ens4 gso off tso off gro off; "
    )

    data["h1"]["runner"] = runner(data["h1"]["popen"], noproc=False)
    data["h2"]["runner"] = runner(data["h2"]["popen"], noproc=False)

    return data
