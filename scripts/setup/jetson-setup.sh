#!/bin/sh

# Update apt repos
apt-get update && yes | apt-get upgrade

# Make tf directory
mkdir -p /tensorflow/models

# Install protobuf, python, and other libraries
apt-get install -y python3 \
    python3-pip \
    python3-dev \
    git \
    protobuf-compiler \
    python3-pil \
    python3-lxml \
    wget \
    curl \
    libgtk2.0-dev \
    pkg-config \
    unzip \
    zip
pip3 install --upgrade pip

# Install tensorflow
pip3 install tensorflow==2.*

# Install python packages
pip3 install matplotlib \
    tf_slim \
    pycocotools \
    opencv-python \
    opencv-contrib-python \
    jupyter -U \
    jupyterlab

# Clone tfod api
git clone https://github.com/tensorflow/models.git /tensorflow/models

# Set working directory
cd /tensorflow/models/research

# Compile protos
protoc object_detection/protos/*.proto --python_out=.

# Copy and install tfod api
cp object_detection/packages/tf2/setup.py .
python3 -m pip install .

# Test tfod installation
python3 object_detection/builders/model_builder_tf2_test.py

# Make tf directory
mkdir -p /tensorflow/workspace
