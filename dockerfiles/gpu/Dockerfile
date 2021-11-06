# Dockerfile for tfod-api enabled workspace
# Author: @edurso

# Use nvidia tensorflow image
FROM nvcr.io/nvidia/tensorflow:21.10-tf2-py3

# Update apt repos
RUN apt-get update && yes | apt-get upgrade

# Make tf directory
RUN mkdir -p /tensorflow/models

# Install protobuf, python, and other libraries
RUN apt-get install -y python3 \
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
RUN pip3 install --upgrade pip

# Install bazel
COPY bazel-install.sh bazel-install.sh
RUN chmod +x ./bazel-install.sh 
RUN bash ./bazel-install.sh

# Install tensorflow
RUN pip3 install tensorflow==2.*

# Install python packages
RUN pip3 install matplotlib \
        tf_slim \
        pycocotools \
        opencv-python \
        opencv-contrib-python \
        jupyter -U \
        jupyterlab \
        tensorflow-io

# Clone tfod api
RUN git clone https://github.com/tensorflow/models.git /tensorflow/models

# Set working directory
WORKDIR /tensorflow/models/research

# Compile protos
RUN protoc object_detection/protos/*.proto --python_out=.

# Copy and install tfod api
RUN cp object_detection/packages/tf2/setup.py .
RUN python3 -m pip install . 

# Test tfod installation
RUN python3 object_detection/builders/model_builder_tf2_test.py

# Make tf directory, will mount dataset here when contanier is run
RUN mkdir -p /tensorflow/workspace

# Set working directory
WORKDIR /tensorflow

# Open port 8888 for jupyter lab
EXPOSE 8888

# Open port 6006 for TensorBoard
EXPOSE 6006

# Jupyter lab
ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]
