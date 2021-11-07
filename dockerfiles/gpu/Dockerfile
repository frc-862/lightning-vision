# Dockerfile for tfod-api enabled workspace
# Author: @edurso

# Use nvidia tensorflow image
FROM nvcr.io/nvidia/tensorflow:21.10-tf2-py3

# Make tf directory
RUN mkdir -p /tensorflow/models

# Setup capabilties for cuda
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.0"
ENV CUDA_VERSION 10.2

# Install common packages
RUN apt-get update && \
    apt-get install -y \
    apt-utils \
    automake \
    build-essential \
    bzip2 \
    ca-certificates \
    curl \
    dnsutils \
    file \
    freeglut3-dev \
    git \
    gnupg2 \
    hdf5-tools \
    htop \
    iotop \
    iputils-ping \
    less \
    libcurl3-dev \
    libfreetype6-dev \
    libglu1-mesa \
    libglu1-mesa-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libjpeg8-dev \
    libpng-dev \
    libtool \
    libx11-dev \
    libxi-dev \
    libxmu-dev \
    libzmq3-dev \
    mlocate \
    nano \
    net-tools \
    nmap \
    ntp \
    openjdk-8-jdk\
    openjdk-8-jre-headless \
    patch \
    pkg-config \
    procps \
    python \
    python-dev \
    python3-pip \
    python3-dev \
	protobuf-compiler \
    python3-pil \
    python3-lxml \
    rsync \
    software-properties-common \
    sudo \
    swig \
    telnet \
    unzip \
    vim \
    wget \
    zip \
    zlib1g-dev \
    && \
    apt-get clean
RUN python3 -m pip install --upgrade pip

# Install tensorflow
RUN pip install tensorflow==2.*

# Test tensorflow installation
RUN python3 -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

# Install python packages
RUN pip3 install matplotlib \
	tf_slim \
	pycocotools \
	opencv-python \
	opencv-contrib-python \
	jupyter -U \
	jupyterlab

# Build & install bazel 
# RUN curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1xeUKKZeQMz_37DTzBUUXl01m-Nv97WZO" > /dev/null \
#     && CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)" \
#     && curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1xeUKKZeQMz_37DTzBUUXl01m-Nv97WZO" -o bazel \
#     && sudo chmod +x bazel \
#     && sudo cp ./bazel /usr/local/bin \
#     && rm ./bazel

RUN pip3 install --extra-index-url https://snapshots.linaro.org/ldcg/python-cache/ tensorflow-io

RUN wget https://files.pythonhosted.org/packages/ec/45/be407a60068204dd5248dae5a4d325370d9b1b3c2cb2a1adb0d673a0d3ae/dm-tree-0.1.6.tar.gz \
    && tar -xvzf dm-tree-0.1.6.tar.gz && rm dm-tree-0.1.6.tar.gz \
    && cd dm-tree-0.1.6/ \
    && pip3 install .

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
