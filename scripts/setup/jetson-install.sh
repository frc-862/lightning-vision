#!/bin/bash

sudo apt install -y \
    python3-pip \
    protobuf-compiler \
    apt-utils \
    automake \
    build-essential \
    curl \
    git \
    net-tools \
    nmap \
    ntp \
    patch \
    pkg-config \
    python3-pil \
    python3-lxml \
    software-properties-common \
    telnet \
    unzip \
    vim \
    wget \
    zip

sudo pip3 install \
    matplotlib \
	tf_slim \
	pycocotools \
	opencv-python \
	opencv-contrib-python \
	jupyter -U \
	jupyterlab

sudo pip3 install --extra-index-url https://snapshots.linaro.org/ldcg/python-cache/ tensorflow-io tensorflow
sudo wget https://github.com/deepmind/tree/archive/refs/tags/0.1.6.tar.gz
sudo tar -xvzf 0.1.6.tar.gz
cd tree-0.1.6/ && python3 setup.py install
sudo rm -rf tree-0.1.6/

if [ ! -d "/tensorflow/models/.git" ]; then
    sudo git clone https://github.com/tensorflow/models.git /tensorflow/models
fi

if [ ! -d "/tensorflow/workspace/.git" ]; then
    sudo git clone https://github.com/edurso/tfod-wkspc.git /tensorflow/workspace
else
    cd /tensorflow/workspace
    git pull
fi

cd /tensorflow/models/research
sudo protoc object_detection/protos/*.proto --python_out=.
sudo cp object_detection/packages/tf2/setup.py .
sudo pip3 install . 

sudo python3 object_detection/builders/model_builder_tf2_test.py
