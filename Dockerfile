FROM python:3.7
MAINTAINER Kuzmenko Ihor <0585ec@gmail.com>

### Installing OpenCV ###
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
        python-tk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install numpy

WORKDIR /
ENV OPENCV_VERSION="4.1.1"
RUN wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
    && unzip ${OPENCV_VERSION}.zip \
    && mkdir /opencv-${OPENCV_VERSION}/cmake_binary \
    && cd /opencv-${OPENCV_VERSION}/cmake_binary \
    && cmake -DBUILD_TIFF=ON \
      -DBUILD_opencv_java=OFF \
      -DWITH_CUDA=OFF \
      -DWITH_OPENGL=ON \
      -DWITH_OPENCL=ON \
      -DWITH_IPP=ON \
      -DWITH_TBB=ON \
      -DWITH_EIGEN=ON \
      -DWITH_V4L=ON \
      -DBUILD_TESTS=OFF \
      -DBUILD_PERF_TESTS=OFF \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DCMAKE_INSTALL_PREFIX=$(python3.7 -c "import sys; print(sys.prefix)") \
      -DPYTHON_EXECUTABLE=$(which python3.7) \
      -DPYTHON_INCLUDE_DIR=$(python3.7 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
      -DPYTHON_PACKAGES_PATH=$(python3.7 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
      .. \
    && make install \
    && rm /${OPENCV_VERSION}.zip \
    && rm -r /opencv-${OPENCV_VERSION}
RUN ln -s \
  /usr/local/python/cv2/python-3.7/cv2.cpython-37m-x86_64-linux-gnu.so \
  /usr/local/lib/python3.7/site-packages/cv2.so

### Installing Tensorflow models ###
## INSTALL tf-slim
#RUN git clone https://github.com/google-research/tf-slim.git
#RUN cd tf-slim && pip install .
#
#### Installing Protobuf ###
#RUN wget https://github.com/google/protobuf/releases/download/v3.3.0/protoc-3.3.0-linux-x86_64.zip \
#    && unzip protoc-3.3.0-linux-x86_64.zip
#ENV PATH_TO_PROTOC /include/google/protobuf/
#RUN pip install matplotlib numpy scikit-image scipy
#
#RUN git clone https://github.com/tensorflow/models.git
#ENV PYTHONPATH $PYTHONPATH:/models/research
#
#WORKDIR /models/research/delf
#RUN /bin/protoc delf/protos/*.proto --python_out=.
#RUN pip install -e .
#WORKDIR /models/research/object_detection
#RUN /bin/protoc protos/*.proto --python_out=./
#WORKDIR /

RUN apt-get update && yes | apt-get upgrade
#RUN apt-get install -y git python-pip
#RUN pip install --upgrade pip
RUN pip install tensorflow
RUN apt-get install -y protobuf-compiler python-pil python-lxml

### Installinf Protob
WORKDIR /TensorFlow
RUN git clone https://github.com/tensorflow/models.git
WORKDIR /TensorFlow/models/research
#RUN protoc object_detection/protos/*.proto --python_out=.
RUN pip install .
WORKDIR /

### Installing Python dependencies ###
ENV PYTHONUNBUFFERED 1
RUN mkdir /wages
WORKDIR /wages
ADD . .
RUN pip install -r requirements.txt
EXPOSE 8000
