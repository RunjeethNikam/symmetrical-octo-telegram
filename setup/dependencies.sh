#!/bin/bash
#
# dependencies.sh
# 
# This script sets up a development environment with essential tools and packages.

# Display system information
uname -a

# Install Iperf3
echo "Installing Iperf3"
sudo apt install iperf3 -y

# Install TShark (commented out)
# echo "Installing TShark"
# sudo apt install tshark -y

# Install Net Tools
echo "Installing Net Tools"
sudo apt install net-tools -y

# Install Unzip
echo "Installing Unzip"
sudo apt install unzip -y

# Remove unnecessary packages
echo "Removing unnecessary packages"
sudo apt autoremove -y

# Install TCP trace
echo "Installing TCP trace"
sudo apt install tcptrace -y

# Install Python3 and pip
echo "Installing python3 pip"
sudo apt install python3-pip -y

# Install Python packages from requirements.txt
echo "Installing python packages"
pip3 install -r ../requirements.txt

# Additional Python packages
echo "Installed matplotlib"
sudo apt-get install -y python-termcolor
sudo apt-get install -y python-matplotlib

# Install IPRoute2
wget http://launchpadlibrarian.net/306560390/iproute2_4.9.0-1ubuntu1_amd64.deb
sudo dpkg -i iproute2_4.9.0-1ubuntu1_amd64.deb
echo "Installed IPRoute"

# Install captcp
echo "Installing captcp"
wget https://github.com/hgn/captcp/archive/master.zip
unzip master.zip
cd captcp-master
sudo make install
echo "Installed captcp"

# Generate SSH key pair
ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''

echo "Setup completed successfully"
