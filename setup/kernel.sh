#!/bin/bash
# kernel.sh
# 
# This script updates the system, installs BBR into the VM, and reboots the system.

# Update the system
echo "####################### Updating the system #######################"
sudo cp /etc/apt/sources.list /etc/apt/sources.list~
sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
sudo apt-get -y update
sudo apt-get -y build-dep linux
sudo apt-get -y upgrade
echo "####################### System Update Complete #######################"

# Install BBR into the VM
echo "####################### Installing BBR into the VM ####################### "
cd /usr/src && sudo chmod 1777 .
# Clone the linux stable repo
git clone https://github.com/sammyas/linux-stable
# change dir to the linux-stable repo
cd /usr/src/linux-stable
# Get the config file
wget  https://raw.githubusercontent.com/google/bbr/master/Documentation/config.gce
mv config.gce .config
# Install the old config
make olddefconfig
make prepare
make -j"$(nproc)"
make -j"$(nproc)" modules
# Set the queue discipline
sudo bash -c 'echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf'
sudo bash -c 'echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf'
sudo make -j`nproc` modules_install install
echo "####################### BBR Installation Complete #######################"

# Reboot the system
echo "####################### REBOOTING the System #######################"
sudo reboot now
