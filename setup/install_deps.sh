#!/bin/bash

uname -a
echo "Installing Iperf3"
sudo apt install iperf3 -y
echo "Installing TShark"
sudo apt install tshark -y
echo "Installing Net Tools"
sudo apt install net-tools -y
echo "Installing Unzip"
sudo apt install unzip -y
echo "Removing unnessary packages"
sudo apt autoremove -y
echo "Installing TCP trace"
sudo apt install tcptrace -y
echo "Installing python3 pip"
sudo apt install python3-pip -y
echo "Installing python packages"
pip3 install -r ../requirements.txt
echo "Done"

sudo apt-get install -y python-termcolor
sudo apt-get install -y python-matplotlib
echo "Installed matplotlib"


wget http://launchpadlibrarian.net/306560390/iproute2_4.9.0-1ubuntu1_amd64.deb
sudo dpkg -i iproute2_4.9.0-1ubuntu1_amd64.deb
echo "Installed IPRoute"

echo "Installing captcp"
wget https://github.com/hgn/captcp/archive/master.zip
unzip master.zip
cd captcp-master
sudo make install
echo "installed captcp"

ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''
