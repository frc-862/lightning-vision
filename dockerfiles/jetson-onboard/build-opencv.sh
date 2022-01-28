#!/bin/sh

cd /opt/
# Download and unzip OpenCV and opencv_contrib and delte zip files
wget https://github.com/opencv/opencv/archive/3.4.7.zip 
unzip 3.4.7.zip 
rm 3.4.7.zip 
wget https://github.com/opencv/opencv_contrib/archive/3.4.7.zip 
unzip 3.4.7.zip 
rm 3.4.7.zip
# Create build folder and switch to it
mkdir -p /opt/opencv-3.4.7/build
cd /opt/opencv-3.4.7/build
# Cmake configure
cmake \
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
make -j"$(nproc)" 
# Install to /usr/local/lib
make install
ldconfig 
# Remove OpenCV sources and build folder
rm -rf /opt/opencv-3.4.7
rm -rf /opt/opencv_contrib-3.4.7
