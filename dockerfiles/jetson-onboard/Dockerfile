# Docker Container for NVIDIA Jetson 2gb to work with FRC Libraries
# JetPack 4.6

# Use NVIDIA Base Container for TensorFlow
# https://ngc.nvidia.com/catalog/containers/nvidia:l4t-tensorflow
FROM nvcr.io/nvidia/l4t-tensorflow:r32.6.1-tf2.5-py3

# Build Environment Configuration
ARG DEBIAN_FRONTEND=noninteractive
ARG OPENCV_VERSION=3.4.7
ARG DOWNLOAD_DIR=/temp

# Install System & Python Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git unzip pkg-config zlib1g-dev \
    libjpeg-dev libjpeg8-dev libjpeg-turbo8-dev \
    libpng-dev libtiff-dev libglew-dev \
    libavcodec-dev libavformat-dev libswscale-dev \
    libgtk2.0-dev libgtk-3-dev libcanberra-gtk* \
    python-dev python-numpy python-pip \
    python3-dev python3-numpy python3-pip \
    libxvidcore-dev libx264-dev libgtk-3-dev \
    libtbb2 libtbb-dev libdc1394-22-dev libxine2-dev \
    gstreamer1.0-tools libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-good1.0-dev \
    libv4l-dev v4l-utils v4l2ucp qv4l2 \
    libtesseract-dev libxine2-dev libpostproc-dev \
    libavresample-dev libvorbis-dev \
    libfaac-dev libmp3lame-dev libtheora-dev \
    libopencore-amrnb-dev libopencore-amrwb-dev \
    libopenblas-dev libatlas-base-dev libblas-dev \
    liblapack-dev liblapacke-dev libeigen3-dev gfortran \
    libhdf5-dev libprotobuf-dev protobuf-compiler \
    libgoogle-glog-dev libgflags-dev \
    make \
    curl \
    wget \
    libfreetype6-dev \
    libzmq3-dev \
    rsync \
    vim \
    zip \
    hdf5-tools \
    libhdf5-serial-dev \
    libxml2-dev \
    libxslt-dev \
    python3-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget http://dragon.studio/2021/02/opencv_2021-02-27-1_all.deb &&\
    apt remove libopencv opencv-licenses libopencv-python libtbb-dev libopencv-dev &&\
    apt install ./opencv_2021-02-27-1_all.deb

RUN echo 'deb http://download.opensuse.org/repositories/home:/auscompgeek:/robotpy/Ubuntu_18.04_Ports/ /' | sudo tee /etc/apt/sources.list.d/home:auscompgeek:robotpy.list &&\
    curl -fsSL https://download.opensuse.org/repositories/home:auscompgeek:robotpy/Ubuntu_18.04_Ports/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_auscompgeek_robotpy.gpg > /dev/null &&\
    apt update &&\
    apt install python3-cscore

# COPY ./build-opencv.sh /opt
# RUN chmod +x /opt/build-opencv.sh &&\
#     sh -c "/opt/build-opencv.sh" &&\
#     rm -f /opt/build-opencv.sh

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
    pynetworktables

# Copy Script To Run Camera App (App Itself to be Pushed into Container when Ran)
RUN mkdir -p /app/
COPY ./runCamera.sh /app/
RUN chmod +x /app/runCamera.sh

# Run Application On Entry
ENTRYPOINT ["sh", "-c",  "./app/runCamera"]
