#!/bin/bash
# Sets up nvidia jetson nano 2gb to run inference on models

# Make /etc/rc.d/rc.local executable
sudo chmod +x /etc/rc.d/rc.local

# Clone or update repo
if [ ! -d "/tensorflow/workspace/.git" ]; then
    sudo git clone https://github.com/edurso/tfod-wkspc.git /tensorflow/workspace
else
    cd /tensorflow/workspace
    git pull
fi

# sudo docker pull edurs0/tfod-wkspc:latest-jetson
