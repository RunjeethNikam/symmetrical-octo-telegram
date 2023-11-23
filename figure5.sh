#!/bin/bash

run () {
    type=$1
    dir=$2

    oldpwd=$PWD
    mkdir -p $dir
    rm -rf $dir/*

	environment=vms
	flowtype=iperf
	flow=1
	maxq=150

    echo "running $type experiment..."
    echo "########################## Installing python package manager ##########################"
    sudo apt install python3-pip -y
    echo "########################## Installing Iper3 package ##########################"
    sudo apt install iperf3 -y
    echo "########################## Installing TShark package ##########################"
    sudo apt install tshark -y
    echo "########################## Installing Net Tools ##########################"
    sudo apt install net-tools -y
    echo "########################## Removing Unnessary packages ##########################"
    sudo apt autoremove
    echo "########################## Installing Python packages ##########################"
    pip3 install -r requirements.txt
    echo "##########################Done##########################"
    echo "########################## Retriving the Destination IP address ##########################"
    destip=`su $SUDO_USER -c "cat ~/.bbr_pair_ip"`
    python3 flows.py --fig-num 5 --time 20 --dest-ip $destip --bw-net 10 --delay 20 --maxq $maxq --environment $environment --flow-type $flowtype --dir $dir
    chmod -R 0777 $dir

    echo "########################## Sanitizing the data ##########################"
    su $SUDO_USER -c "tshark -2 -r $dir/flow_bbr.dmp -R 'tcp.stream eq $flow && tcp.analysis.ack_rtt'  -e frame.time_relative -e tcp.analysis.ack_rtt -Tfields -E separator=, > $dir/bbr_rtt.txt"
    su $SUDO_USER -c "tshark -2 -r $dir/flow_cubic.dmp -R 'tcp.stream eq $flow && tcp.analysis.ack_rtt'  -e frame.time_relative -e tcp.analysis.ack_rtt -Tfields -E separator=, > $dir/cubic_rtt.txt"
    echo "########################## Done ##########################"

    echo "########################## Plotting the results ##########################"
    python3 plot_ping.py -f $dir/bbr_rtt.txt $dir/cubic_rtt.txt --xlimit 8 -o $dir/figure5_$type.png
    echo "########################## Done ##########################"
}

run "iperf" figure5_iperf
