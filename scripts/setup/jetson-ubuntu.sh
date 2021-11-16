#!/bin/bash

# For This Disk Image: https://cdimage.ubuntu.com/focal/daily-live/current/focal-desktop-arm64.iso

# Check GPU
lspci | grep -i nvidia

# Check Linux Distro
uname -m && cat /etc/*release

# Install Pre-Reqs
sudo apt-get update
sudo apt-get install -y \
    linux-headers-$(uname -r) \
    make \
    gcc \
    g++

# Install CUDA - From https://developer.nvidia.com/cuda-downloads
# To Remove: sudo apt-get --purge remove cuda
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/sbsa/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda-repo-ubuntu2004-11-5-local_11.5.0-495.29.05-1_arm64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-5-local_11.5.0-495.29.05-1_arm64.deb
sudo apt-key add /var/cuda-repo-ubuntu2004-11-5-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda
sudo apt-get -y install cuda-drivers

# Install Docker
curl https://get.docker.com | sh
sudo systemctl --now enable docker

# Setup Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2

# Restart Docker
sudo systemctl restart docker

# Test With CUDA Base Container
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
