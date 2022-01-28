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
    -DCMAKE_BUILD_TYPE=RELEASE \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DOPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib/modules \
    -DEIGEN_INCLUDE_PATH=/usr/include/eigen3 \
    -DWITH_OPENCL=OFF \
    -DWITH_CUDA=ON \
    -DCUDA_ARCH_PTX="" \
    -DWITH_CUDNN=ON \
    -DWITH_CUBLAS=ON \
    -DENABLE_FAST_MATH=ON \
    -DCUDA_FAST_MATH=ON \
    -DOPENCV_DNN_CUDA=ON \
    -DENABLE_NEON=ON \
    -DWITH_QT=OFF \
    -DWITH_OPENMP=ON \
    -DBUILD_TIFF=ON \
    -DWITH_FFMPEG=ON \
    -DWITH_GSTREAMER=ON \
    -DWITH_TBB=ON \
    -DBUILD_TBB=ON \
    -DBUILD_TESTS=OFF \
    -DWITH_EIGEN=ON \
    -DWITH_V4L=ON \
    -DWITH_LIBV4L=ON \
    -DOPENCV_ENABLE_NONFREE=ON \
    -DINSTALL_C_EXAMPLES=OFF \
    -DINSTALL_PYTHON_EXAMPLES=OFF \
    -DPYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
    -DOPENCV_GENERATE_PKGCONFIG=ON \
    -DBUILD_EXAMPLES=OFF \
    ..

# Make
make -j"$(nproc)" 

# Install to /usr/local/lib
make install
ldconfig 

# Remove OpenCV sources and build folder
rm -rf /opt/opencv-3.4.7
rm -rf /opt/opencv_contrib-3.4.7
