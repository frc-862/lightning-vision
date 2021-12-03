#!/bin/bash
# Sets up nvidia jetson to develop models

# Install labelImg for labeling datasets
sudo pip3 install labelImg

# Clone or update repo
if [ ! -d "/tensorflow/workspace/.git" ]; then
    sudo git clone https://github.com/edurso/tfod-wkspc.git /tensorflow/workspace
    cd /tensorflow/workspace
else
    cd /tensorflow/workspace
    sudo git pull
fi

sudo docker pull edurs0/tfod-wkspc:latest-jetson
