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
    python3-pip \
    python3-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install -U pip -v

RUN pip3 --no-cache-dir install -U -v \
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
	google-pasta

RUN pip3 --no-cache-dir install --pre -v --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 \
	tensorflow==2.5.0+nv21.7

EXPOSE 8888 6006

RUN mkdir -p /tensorflow/workspace

CMD ["jupyter", "lab", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--notebook-dir='/tensorflow/workspace'"]
