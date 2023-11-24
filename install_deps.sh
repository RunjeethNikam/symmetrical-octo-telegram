#!/bin/bash

uname -a
sudo apt install iperf3 -y
sudo apt install tshark -y
sudo apt install net-tools -y
sudo apt install unzip -y
sudo apt autoremove -y
sudo apt install tcptrace

sudo apt install python3-pip -y
pip3 install -r requirements.txt

sudo apt-get install -y python-termcolor
sudo apt-get install -y python-matplotlib


wget http://launchpadlibrarian.net/306560390/iproute2_4.9.0-1ubuntu1_amd64.deb
sudo dpkg -i iproute2_4.9.0-1ubuntu1_amd64.deb

wget https://github.com/hgn/captcp/archive/master.zip
unzip master.zip
cd captcp-master
sudo make install

ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''
