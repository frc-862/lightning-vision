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

RUN mkdir -p ${DOWNLOAD_DIR}
RUN cd /opt/
    # Download and unzip OpenCV and opencv_contrib and delte zip files
RUN wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip 
RUN unzip $OPENCV_VERSION.zip 
RUN rm $OPENCV_VERSION.zip 
RUN wget https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip 
RUN unzip ${OPENCV_VERSION}.zip 
RUN rm ${OPENCV_VERSION}.zip
    # Create build folder and switch to it
RUN mkdir /opt/opencv-${OPENCV_VERSION}/build && cd /opt/opencv-${OPENCV_VERSION}/build
    # Cmake configure
RUN cmake \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
        -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
        -D WITH_OPENCL=OFF \
        -D WITH_CUDA=ON \
        #-D CUDA_ARCH_BIN=5.3 \
        -D CUDA_ARCH_PTX="" \
        -D WITH_CUDNN=ON \
        -D WITH_CUBLAS=ON \
        -D ENABLE_FAST_MATH=ON \
        -D CUDA_FAST_MATH=ON \
        -D OPENCV_DNN_CUDA=ON \
        -D ENABLE_NEON=ON \
        -D WITH_QT=OFF \
        -D WITH_OPENMP=ON \
        -D BUILD_TIFF=ON \
        -D WITH_FFMPEG=ON \
        -D WITH_GSTREAMER=ON \
        -D WITH_TBB=ON \
        -D BUILD_TBB=ON \
        -D BUILD_TESTS=OFF \
        -D WITH_EIGEN=ON \
        -D WITH_V4L=ON \
        -D WITH_LIBV4L=ON \
        -D OPENCV_ENABLE_NONFREE=ON \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
        -D OPENCV_GENERATE_PKGCONFIG=ON \
        -D BUILD_EXAMPLES=OFF \
        # -DOPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib-${OPENCV_VERSION}/modules \
        # -DWITH_CUDA=ON \
        # -DCMAKE_BUILD_TYPE=RELEASE \
        # # Install path will be /usr/local/lib (lib is implicit)
        # -DCMAKE_INSTALL_PREFIX=/usr/local \
        ..
    # Make
RUN make -j"$(nproc)" 
    # Install to /usr/local/lib
RUN make install
RUN ldconfig 
    # Remove OpenCV sources and build folder
RUN rm -rf /opt/opencv-${OPENCV_VERSION} && rm -rf /opt/opencv_contrib-${OPENCV_VERSION}

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

# TODO Run Application On Entry
ENTRYPOINT ["/app/runCamera.sh"]
