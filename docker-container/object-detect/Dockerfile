FROM balenalib/rpi-raspbian

RUN apt-get update

# install build depedencies
RUN apt-get install build-essential \
    ca-certificates \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    libgtk-3-dev \
    zip \
    libtiff5-dev \
    libjasper-dev \
    libpng12-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libatlas-base-dev \
    libraspberrypi0 \
    unzip

RUN apt-get clean
RUN pip3 install numpy
RUN pip3 install --upgrade setuptools

ENV OPENCV_VERSION 4.1.0

# download opencv
WORKDIR opencv
RUN wget -O opencv.zip https://github.com/Itseez/opencv/archive/$OPENCV_VERSION.zip
RUN unzip opencv.zip
RUN wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/$OPENCV_VERSION.zip
RUN unzip opencv_contrib.zip


# compile opencv
WORKDIR opencv-$OPENCV_VERSION
RUN mkdir build
WORKDIR build
RUN  cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv/opencv_contrib-$OPENCV_VERSION/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

# adjust swap size for compilation
RUN apt-get install -y dphys-swapfile
RUN sed -i 's/CONF_SWAPSIZE=100$/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile
RUN /etc/init.d/dphys-swapfile stop
RUN /etc/init.d/dphys-swapfile start

# install opencv
RUN make -j3
RUN make install
RUN ldconfig

# clean up opencv and reduce the image size by deleting files
WORKDIR /
RUN rm -rf /opencv

# build dlib
WORKDIR /root
RUN git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git
WORKDIR /root/dlib
RUN python3 setup.py install --compiler-flags "-mfpu=neon"

# install other project dependencies with pip
RUN pip3 install face_recognition==1.2.3
RUN pip3 install picamera==1.13
RUN pip3 install imutils==0.4.3
RUN pip3 install pyserial==3.4
