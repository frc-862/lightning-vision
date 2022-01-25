# Docker Container for NVIDIA Jetson 2gb to work with FRC Libraries
# JetPack 4.6

# Use NVIDIA Base Container for TensorFlow
# https://ngc.nvidia.com/catalog/containers/nvidia:l4t-tensorflow
FROM nvcr.io/nvidia/l4t-tensorflow:r32.6.1-tf2.5-py3

# Build Environment Configuration
ARG DEBIAN_FRONTEND=noninteractive

# Install System & Python Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    make \
    curl \
    wget \
    libfreetype6-dev \
    libhdf5-dev \
    libpng-dev \
    libzmq3-dev \
    pkg-config \
    python3-dev \
    rsync \
    vim \
    unzip \
    zlib1g-dev \
    zip \
    libjpeg8-dev \
    hdf5-tools \
    libhdf5-serial-dev \
    protobuf-compiler \
    libxml2-dev \
    libxslt-dev \
    python3-pip \
    python3-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python Packages
RUN pip3 install -U pip -v \ 
    && pip3 install --no-cache-dir install -U -v \
    numpy==1.19.5 \
    pandas==1.1.5 \
    scipy==1.5.4 \
    matplotlib==3.3.4 \
    six mock \
    requests \
    termcolor \
    protobuf \
    keras \
    keras-applications \
    keras-preprocessing \
    google-pasta \
    opencv-python \
    pynetworktables

# Copy Script To Run Camera App (App Itself to be Pushed into Container when Ran)
RUN mkdir -p /app/
COPY ./runCamera /app/
RUN chmod +x /app/runCamera

# TODO Run Application On Entry
ENTRYPOINT [ "exec" "/app/runCamera" ]
