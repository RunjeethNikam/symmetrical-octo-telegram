import os
import json
from subprocess import Popen as Pn
from multiprocessing import Process

from ip_utils import get_ip_address, start_ping
SU = 'SUDO_USER'

def build_topology(args):
    def crt_rnner(popen, np=False):
        def execute_command(cmd, background=False, daemon=True):
            if np:
                process = Pn(cmd, shell=True)
                if not background:
                    return process.wait()

            def start_command():
                Pn(cmd, shell=True).wait()

            process = Process(target=start_command)
            process.daemon = daemon
            process.start()
            if not background:
                process.join()
            return process

        return execute_command

    def ssh_popen(command, *args, **kwargs):
        user = os.environ.get(SU, os.environ["USER"])
        host_ip = data["host_2"]["IP"]
        full_command = f"ssh -o StrictHostKeyChecking=no -i /home/{user}/.ssh/id_rsa {user}@{host_ip} 'sudo bash -c {json.dumps(command)}'"
        kwargs["shell"] = True
        return Pn(full_command, *args, **kwargs)

    data = {
        "type": "emulator",
        "host_1": {
            "IP": get_ip_address(args.dest_ip),
            "popen": Pn,
        },
        "host_2": {
            "IP": args.dest_ip,
            "popen": ssh_popen,
        },
        "obj": None,
    }

    host_2_runner = crt_rnner(data["host_2"]["popen"], np=False)
    host_1_runner = crt_rnner(data["host_1"]["popen"], np=False)

    ift = (
        "modprobe ifb numifbs=1; "
        "ip link set dev ifb0 up; "
        "ifconfig ifb0 txqueuelen 1000; "
        "tc qdisc del dev {iface} ingress; "
        "tc qdisc add dev {iface} handle ffff: ingress; "
        "tc filter add dev {iface} parent ffff: protocol all u32 match u32 0 0 action mirred egress redirect dev ifb0; "
    )
    pf = (
        "tc qdisc del dev {iface} root; "
        "tc qdisc add dev {iface} root handle 1: htb default 10; "
        "tc class add dev {iface} parent 1: classid 1:10 htb rate {rate}Mbit; "
        "tc qdisc add dev {iface} parent 1:10 handle 20: netem delay {delay}ms limit {queue}; "
    )
    

    pipeline_arguments = {"rate": args.bw_net, "delay": args.delay, "queue": args.maxq}
    host_2_runner(
        ift.format(iface="ens4")
        + pf.format(iface="ens4", **pipeline_arguments)
        + pf.format(iface="ifb0", **pipeline_arguments)
        + "sudo ethtool -K ens4 gso off tso off gro off; "
        "sudo ethtool -K ifb0 gso off tso off gro off; "
    )
    host_1_runner(
        "tc qdisc del dev ens4 root; "
        "tc qdisc add dev ens4 root fq pacing; "
        "sudo ethtool -K ens4 gso off tso off gro off; "
    )

    data["host_1"]["runner"] = crt_rnner(data["host_1"]["popen"], np=False)
    data["host_2"]["runner"] = crt_rnner(data["host_2"]["popen"], np=False)

    return data
