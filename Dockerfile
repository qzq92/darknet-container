FROM nvcr.io/nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

RUN apt-get update && apt-get install -y build-essential vim make cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev

# Install opencv dependencies
WORKDIR /dependencies

COPY ./dependencies /dependencies

RUN cd opencv && \
    mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_GENERATE_PKGCONFIG=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/dependencies/opencv_contrib/modules \
	-D BUILD_EXAMPLES=ON .. && \
    make -j$(nproc) && \
    make install

# Install Darknet
WORKDIR /darknet

COPY ./darknet /darknet

ARG arch='-gencode arch=compute_50,code=[sm_50,compute_50] -gencode arch=compute_52,code=[sm_52,compute_52] -gencode arch=compute_60,code=[sm_60,compute_60] -gencode arch=compute_61,code=[sm_61,compute_61] -gencode arch=compute_70,code=[sm_70,compute_70] -gencode arch=compute_75,code=[sm_75,compute_75]'

# Refer to darknet Makefile for options based on hardware
# RTX 2070
RUN make GPU=1 CUDNN=1 CUDNN_HALF=1 OPENCV=1 LIBSO=1 ARCH=' ${arch}'

# Tesla V100
#RUN make GPU=1 CUDNN=1 CUDNN_HALF=1 OPENCV=1 LIBSO=1 ARCH=' -gencode arch=compute_70,code=[sm_70,compute_70]'

ENTRYPOINT ["/bin/bash"]
