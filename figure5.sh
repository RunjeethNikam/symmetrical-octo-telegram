#!/bin/bash

run () {
    type=iperf
    dir=./figures
    oldpwd=$PWD

    echo "Making the figures directory"
    mkdir -p $dir
    rm -rf $dir/*

	flow=1
	maxq=150

    echo "running $type experiment..."

    echo "########################## Retriving the Destination IP address ##########################"
    destip=`su $SUDO_USER -c "cat ~/.bbr_pair_ip"`
    echo "################ Done #####################"
    echo "Getting the metrics"
	pip3 install -r requirements.txt
    python3 flows.py --time 20 --dest-ip $destip --bw-net 10 --delay 20 --maxq $maxq --environment vms --flow-type iperf --dir $dir
    chmod -R 0777 $dir
    echo "Done"

    echo "########################## Sanitizing the data ##########################"
    su $SUDO_USER -c "tshark -2 -r $dir/flow_bbr.dmp -R 'tcp.stream eq $flow && tcp.analysis.ack_rtt'  -e frame.time_relative -e tcp.analysis.ack_rtt -Tfields -E separator=, > $dir/bbr_rtt.txt"
    su $SUDO_USER -c "tshark -2 -r $dir/flow_cubic.dmp -R 'tcp.stream eq $flow && tcp.analysis.ack_rtt'  -e frame.time_relative -e tcp.analysis.ack_rtt -Tfields -E separator=, > $dir/cubic_rtt.txt"
    echo "########################## Done ##########################"

    echo "########################## Plotting the results ##########################"
    python3 plot_ping.py -f $dir/bbr_rtt.txt $dir/cubic_rtt.txt --xlimit 20 -o $dir/figure5_$type.png
    echo "########################## Done ##########################"
}

run "iperf" figure5_iperf
