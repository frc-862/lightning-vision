# Dockerfile for tfod-api enabled workspace
# Author: @edurso

# Use tensorflow image
FROM tensorflow/tensorflow:latest

# Update apt repos
RUN apt-get update && yes | apt-get upgrade

# Make tf directory
RUN mkdir -p /tensorflow/models

# Install/update python3 & pip3
RUN apt-get install -y python3 \
    python3-pip \
    git
RUN pip3 install --upgrade pip

# Install tensorflow
RUN pip3 install tensorflow==2.*

# Install protobuf and other libraries
RUN apt-get install -y protobuf-compiler \
    python3-pil \
    python3-pil \
    python3-lxml \
    wget \
    curl \
    libgtk2.0-dev \
    pkg-config

# Install python packages
RUN pip3 install matplotlib \
    tf_slim \
    pycocotools \
    labelImg \
    opencv-python \
    opencv-contrib-python \
    jupyter -U \
    jupyterlab 

# Clone tfod api
RUN git clone https://github.com/tensorflow/models.git /tensorflow/models

# Set working directory
WORKDIR /tensorflow

# Compile protos
RUN protoc models/research/object_detection/protos/*.proto --python_out=.

# Copy and install tfod api
RUN cp models/research/object_detection/packages/tf2/setup.py .
RUN python3 -m pip install .

# Test tfod installation
RUN python3 object_detection/builders/model_builder_tf2_test.py

# Install git lfs
RUN cd &&\
    wget https://github.com/git-lfs/git-lfs/releases/download/v2.13.3/git-lfs-linux-amd64-v2.13.3.tar.gz &&\
	mkdir git-lfs-install &&\
	cd git-lfs-install &&\
	tar -xzf ../git-lfs-linux-amd64-v2.13.3.tar.gz &&\
	sudo ./install.sh &&\
	cd &&\
	rm -rf git-lfs-linux-amd64-v2.13.3.tar.gz git-lfs-install &&\
	git lfs install

# Clone tfod-wkspc
RUN git clone https://github.com/edurso/tfod-wkspc.git /tensorflow/workspace

# Set working directory
WORKDIR /tensorflow/workspace

# Open port 8888 for jupyter lab
EXPOSE 8888

# Jupyter lab
ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]

