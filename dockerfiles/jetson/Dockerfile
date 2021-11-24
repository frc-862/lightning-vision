FROM nvcr.io/nvidia/l4t-tensorflow:r32.6.1-tf2.5-py3

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
    protobuf-compiler \
    git \
    && python3 -m pip install --upgrade pip

RUN mkdir -p /tensorflow/models \
    && git clone https://github.com/tensorflow/models.git /tensorflow/models
WORKDIR /tensorflow/models/research

RUN protoc object_detection/protos/*.proto --python_out=. \
    && cp object_detection/packages/tf2/setup.py . \
    && pip3 install --no-deps . 

RUN pip3 install \
    tf_slim \
    scipy

RUN python3 object_detection/builders/model_builder_tf2_test.py

RUN mkdir -p /tensorflow/workspace
WORKDIR /tensorflow/workspace
