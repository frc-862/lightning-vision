# Dockerfile for tfod-api enabled workspace

# Use nvidia tensorflow image
FROM nvcr.io/nvidia/l4t-tensorflow:r32.6.1-tf2.5-py3

# Make tf directory
RUN mkdir -p /tensorflow/models

# Environment vars and args
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Detroit

# Setup for cuda
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# Install common packages
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    vim \
    wget \
    curl \
    protobuf-compiler \
    git \
    zip
RUN python3 -m pip install --upgrade pip

# Clone tfod api
RUN git clone https://github.com/tensorflow/models.git /tensorflow/models

# Set working directory
WORKDIR /tensorflow/models/research

# Compile protos
RUN protoc object_detection/protos/*.proto --python_out=.

# Install bazel & python packages
RUN wget -O /usr/bin/bazel https://github.com/bazelbuild/bazel/releases/download/3.7.2/bazel-3.7.2-linux-arm64 \
    && chmod +x /usr/bin/bazel \
    && alias bazel="/usr/bin/bazel"
RUN wget https://github.com/deepmind/tree/archive/refs/tags/0.1.6.tar.gz \
    && tar -xvzf 0.1.6.tar.gz \
    && cd tree-0.1.6/ \
    && python3 setup.py install \
    && cd .. && rm -rf tree-0.1.6/ 0.1.6.tar.gz \
    && pip3 install https://snapshots.linaro.org/ldcg/python-cache/tensorflow-io-gcs-filesystem/tensorflow_io_gcs_filesystem-0.20.0-cp36-cp36m-linux_aarch64.whl \
    # && wget https://github.com/tensorflow/io/archive/refs/tags/v0.18.0.tar.gz \
    # && tar -xvzf v0.18.0.tar.gz \
    # && cd io-0.18.0/ \
    # && python3 setup.py install \
    # && cd .. && rm -rf io-0.18.0/ v0.18.0.tar.gz \
    && wget https://github.com/tensorflow/addons/archive/refs/tags/v0.15.0.tar.gz \
    && tar -xvzf v0.15.0.tar.gz \
    && cd addons-0.15.0/ \
    && python3 setup.py install \
    && cd .. && rm -rf addons-0.15.0/ v0.15.0.tar.gz \
    && pip3 install pycocotools \
    opencv-python \
    opencv-contrib-python \
    jupyter -U \
    jupyterlab \
    tf-models-official 

# Test tensorflow installation
RUN python3 -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

# Copy and install tfod api
RUN cp object_detection/packages/tf2/setup.py . \
    && python3 -m pip install . 

# Test tfod installation
RUN python3 object_detection/builders/model_builder_tf2_test.py

# Make tf directory, will mount dataset here when contanier is run
RUN mkdir -p /tensorflow/workspace

# Set working directory
WORKDIR /tensorflow

# Open port 8888 for jupyter lab
EXPOSE 8888

# Open port 6006 for tensorboard
EXPOSE 6006

# Jupyter lab
ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]
