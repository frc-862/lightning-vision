# Dockerfile for tfod-api enabled workspace
# Author: @edurso

# Use https://github.com/ml-tooling/ml-workspace image
FROM mltooling/ml-workspace:latest

# Update apt repos
RUN apt-get update && yes | apt-get upgrade

# Make tf directory
RUN mkdir -p /tensorflow/models

# Install/update python3 & pip3
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN pip3 install --upgrade pip

# Install tensorflow
RUN pip3 install tensorflow==2.*

# Install protobuf and other libraries
RUN apt-get install -y protobuf-compiler
RUN apt-get install -y python3-pil
RUN apt-get install -y python3-lxml
RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y libgtk2.0-dev
RUN apt-get install -y pkg-config
RUN pip3 install matplotlib
RUN pip3 install tf_slim
RUN pip3 install pycocotools
RUN pip3 install labelImg
RUN pip3 install opencv-python
RUN pip3 install opencv-contrib-python

# Clone tfod api
RUN git clone https://github.com/tensorflow/models.git /root/Desktop/workspace/tensorflow/models

# Set working directory
WORKDIR /root/Desktop/workspace/tensorflow/models/research

# Get rid of unused tutorials
RUN rm -rf /root/Desktop/workspace/tutorials

# Compile protos
RUN protoc object_detection/protos/*.proto --python_out=.

# Copy and install tfod api
RUN cp object_detection/packages/tf2/setup.py .
RUN python3 -m pip install .

# Test tfod installation
RUN python3 object_detection/builders/model_builder_tf2_test.py

