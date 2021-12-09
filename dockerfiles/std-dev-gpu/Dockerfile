# Docker Container for General Use on GPU Enabled Machines

# Use TensorFlow 2.5.0 Base GPU Container
# https://hub.docker.com/r/tensorflow/tensorflow
FROM tensorflow/tensorflow:2.5.0-gpu

# Build Environment Configuration
ARG DEBIAN_FRONTEND=noninteractive

# Install System & Python Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    make \
    curl \
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
    git \
    python3-pip \
    python3-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install -U pip -v \ 
    && pip3 install --no-cache-dir install -U -v \
    numpy==1.19.5 \
    pandas==1.1.5 \
    scipy==1.5.4 \
    jupyterlab==2.2.9 \
    matplotlib==3.3.4 \
    six mock \
    requests \
    termcolor \
    protobuf \
    keras \
    keras-applications \
    keras-preprocessing \
    google-pasta

# Install Bazel (a little sketchy, but it works ¯\_(ツ)_/¯)
RUN wget -O /usr/bin/bazel https://github.com/bazelbuild/bazel/releases/download/3.7.2/bazel-3.7.2-linux-x86_64 \
    && chmod +x /usr/bin/bazel \
    && alias bazel="/usr/bin/bazel"

# Install `tensorflow-addons` (build from source)
RUN wget https://github.com/tensorflow/addons/archive/refs/tags/v0.13.0.tar.gz \
    && tar -xvzf v0.13.0.tar.gz \
    && cd addons-0.13.0/ \
    && python3 setup.py install \
    && cd .. && rm -rf addons-0.13.0/ v0.13.0.tar.gz

# Install `tensorflow-io` & `tensorflow-io-gcs-filesystem` (build from source)
RUN wget https://github.com/tensorflow/io/archive/refs/tags/v0.19.1.tar.gz \
    && tar -xvzf v0.19.1.tar.gz && cd io-0.19.1/ \
    && chmod +x ./configure.sh \
    && ./configure.sh \
    && python3 setup.py -q bdist_wheel --project tensorflow_io_gcs_filesystem \
    && cd dist && pip3 install $(ls | grep *.whl) \
    && cd .. && pip3 install . \
    && cd .. && rm -rf v0.19.1.tar.gz io-0.19.1/
    
# Setup Official TensorFlow Models Repo
RUN mkdir -p /tensorflow/models \
    && git clone https://github.com/tensorflow/models.git /tensorflow/models

# Install TensorFlow `object-detection` Package from Models Repo 
WORKDIR /tensorflow/models/research
RUN protoc object_detection/protos/*.proto --python_out=. \
    && cp object_detection/packages/tf2/setup.py . \
    && pip3 install .

# Test Installation
RUN python3 object_detection/builders/model_builder_tf2_test.py

# Open Port 8888 for JupyterLab & Port 6006 for TensorBoard
EXPOSE 8888 6006

# Make Directory for Workspace
RUN mkdir -p /tensorflow/workspace

# Start JupyterLab on Entry
WORKDIR /tensorflow
ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]
