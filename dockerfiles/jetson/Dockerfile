FROM nvcr.io/nvidia/l4t-ml:r32.6.1-py3

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libfreetype6-dev \
    libhdf5-dev \
    libpng-dev \
    libzmq3-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-scipy \
    python3-sklearn \
    python3-matplotlib \
    python3-pandas \
    rsync \
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
    && pip3 install -U pip -v

RUN wget -O /usr/bin/bazel https://github.com/bazelbuild/bazel/releases/download/3.7.2/bazel-3.7.2-linux-arm64 \
    && chmod +x /usr/bin/bazel \
    && alias bazel="/usr/bin/bazel" \
    && wget https://github.com/tensorflow/addons/archive/refs/tags/v0.13.0.tar.gz \
    && tar -xvzf v0.13.0.tar.gz \
    && cd addons-0.13.0/ \
    && python3 setup.py install \
    && cd .. && rm -rf addons-0.13.0/ v0.13.0.tar.gz \
    && wget https://github.com/deepmind/tree/archive/refs/tags/0.1.6.tar.gz \
    && tar -xvzf 0.1.6.tar.gz \
    && cd tree-0.1.6/ \
    && python3 setup.py install \
    && cd .. && rm -rf tree-0.1.6/ 0.1.6.tar.gz

RUN pip3 --no-cache-dir install --pre -v --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 \
    tensorflow==2.5.0+nv21.7 \
    && pip3 --no-cache-dir install -U -v \
    jupyter \
    jupyterlab \
    grpcio \
    absl-py \
    py-cpuinfo \
    psutil \
    portpicker \
    six mock \
    requests \
    gast \
    h5py \
    astor \
    termcolor \
    protobuf \
    keras \
    keras-applications \
    keras-preprocessing \
    wrapt \
    google-pasta \
    tf-models-official==2.6.0


RUN mkdir -p /tensorflow/models \
    && git clone https://github.com/tensorflow/models.git /tensorflow/models
WORKDIR /tensorflow/models/research

RUN wget https://github.com/tensorflow/io/archive/refs/tags/v0.19.1.tar.gz \
    && tar -xvzf v0.19.1.tar.gz && cd io-0.19.1/ \
    && chmod +x ./configure.sh \
    && ./configure.sh \
    && python3 setup.py -q bdist_wheel --project tensorflow_io_gcs_filesystem \
    && cd dist && pip3 install $(ls | grep *.whl) \
    && cd .. && pip3 install . \
    && cd .. && rm -rf io-0.19.1.tar.gz io-0.19.1/

RUN protoc object_detection/protos/*.proto --python_out=. \
    && cp object_detection/packages/tf2/setup.py . \
    && pip3 install .

RUN python3 object_detection/builders/model_builder_tf2_test.py

EXPOSE 8888 6006

RUN mkdir -p /tensorflow/workspace

CMD ["jupyter", "lab", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--notebook-dir='/tensorflow/workspace'"]
