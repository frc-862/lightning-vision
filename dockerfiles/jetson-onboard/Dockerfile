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
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install -U pip -v \ 
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
    google-pasta

# Install OpenCV
# From: https://github.com/JulianAssmann/opencv-cuda-docker/blob/master/ubuntu-20.04/opencv-4.5.3/cuda-11.4.1/Dockerfile
# If this does not work, use the `build_opencv` from wpilibpi but with `-DMAKE_CUDA=ON`
ARG OPENCV_VERSION=3.4.7
ARG DOWNLOAD_DIR=/temp
RUN mkdir -p ${DOWNLOAD_DIR}
RUN cd /opt/ &&\
    # Download and unzip OpenCV and opencv_contrib and delte zip files
    wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip &&\
    unzip $OPENCV_VERSION.zip &&\
    rm $OPENCV_VERSION.zip &&\
    wget https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip &&\
    unzip ${OPENCV_VERSION}.zip &&\
    rm ${OPENCV_VERSION}.zip &&\
    # Create build folder and switch to it
    mkdir /opt/opencv-${OPENCV_VERSION}/build && cd /opt/opencv-${OPENCV_VERSION}/build &&\
    # Cmake configure
    cmake \
        -DOPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib-${OPENCV_VERSION}/modules \
        -DWITH_CUDA=ON \
        -DCMAKE_BUILD_TYPE=RELEASE \
        # Install path will be /usr/local/lib (lib is implicit)
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        .. &&\
    # Make
    make -j"$(nproc)" && \
    # Install to /usr/local/lib
    make install && \
    ldconfig &&\
    # Remove OpenCV sources and build folder
    rm -rf /opt/opencv-${OPENCV_VERSION} && rm -rf /opt/opencv_contrib-${OPENCV_VERSION}

# Download: pynetworktable, robotpy-cscore, & pybind11
RUN cd ${DOWNLOAD_DIR} \
    && wget -nc -nv -O ${DOWNLOAD_DIR}/pynetworktables.tar.gz https://github.com/robotpy/pynetworktables/archive/2021.0.0.tar.gz \
    && wget -nc -nv -O ${DOWNLOAD_DIR}/robotpy-cscore.tar.gz https://github.com/robotpy/robotpy-cscore/archive/2021.0.0.tar.gz \
    && wget -nc -nv -O ${DOWNLOAD_DIR}/robotpy-cscore/pybind11.tar.gz https://github.com/pybind/pybind11/archive/v2.6.1.tar.gz \
    && tar xzf "${DOWNLOAD_DIR}/pynetworktables.tar.gz" \
    && mv ${DOWNLOAD_DIR}/pynetworktables-* ${DOWNLOAD_DIR}/pynetworktables \
    && echo "__version__ = '2021.0.0'" > ${DOWNLOAD_DIR}/pynetworktables/_pynetworktables/_impl/version.py \
    && tar xzf "${DOWNLOAD_DIR}/robotpy-cscore.tar.gz" \
    && mv ${DOWNLOAD_DIR}/robotpy-cscore-* ${DOWNLOAD_DIR}/robotpy-cscore \
    && echo "__version__ = '2021.0.0'" > ${DOWNLOAD_DIR}/robotpy-cscore/cscore/version.py \
    && rm -rf ${DOWNLOAD_DIR}/robotpy-cscore/pybind11 \
    && tar xzf "${DOWNLOAD_DIR}/robotpy-cscore/pybind11.tar.gz" \
    && mv ${DOWNLOAD_DIR}/robotpy-cscore/pybind11-* ${DOWNLOAD_DIR}/robotpy-cscore/pybind11

# Install: pynetworktable, robotpy-cscore, & pybind11
RUN cd ${DOWNLOAD_DIR}/pynetworktables \
    && python3 setup.py build \
    && python3 setup.py install \
    && python3 setup.py clean
RUN cd ${DOWNLOAD_DIR}/robotpy-cscore/pybind11 \
    && python3 setup.py build \
    && python3 setup.py install \
    && python3 setup.py clean
RUN cd ${DOWNLOAD_DIR}/robotpy-cscore \
    && python3 setup.py build \
    && python3 setup.py install \
    && python3 setup.py clean

# Copy Script To Run Camera App (App Itself to be Pushed into Container when Ran)
RUN mkdir -p /app/
COPY ./runCamera /app/
RUN chmod +x /app/runCamera

# TODO Run Application On Entry
ENTRYPOINT [ "exec" "/app/runCamera" ]
