FROM balenalib/rpi-raspbian:buster-20190619

RUN apt-get update
RUN apt-get upgrade

# install build depedencies
RUN apt-get install build-essential \
    ca-certificates \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    zip \
    unzip

RUN apt-get install libpng12-0 -y
RUN apt-get install libgtk-3-dev libcanberra-gtk* libatlas-base-dev gfortran python3-dev -y
RUN apt-get install libjpeg-dev libpng-dev libtiff-dev -y
RUN apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
RUN apt-get install libxvidcore-dev libx264-dev -y
RUN apt-get install libgtk-3-dev -y
RUN apt-get install libcanberra-gtk* -y
RUN apt-get install libatlas-base-dev gfortran -y
RUN apt-get install python3-dev -y

RUN apt-get install  \
    graphicsmagick \
    libatlas-base-dev \
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
    libtiff5-dev \
    libjasper-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libatlas-base-dev \
    libraspberrypi0 -y

RUN apt-get clean
RUN pip3 install numpy
RUN pip3 install wheel
RUN sudo -H pip3 install setuptools --upgrade

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

# install dlib
WORKDIR /root
RUN git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git
WORKDIR /root/dlib
RUN python3 setup.py install --compiler-flags "-mfpu=neon"

# install other project dependencies with pip
RUN wget https://files.pythonhosted.org/packages/fa/37/45185cb5abbc30d7257104c434fe0b07e5a195a6847506c074527aa599ec/Click-7.0-py2.py3-none-any.whl
RUN pip3 install Click-7.0-py2.py3-none-any.whl
RUN pip3 install --no-cache-dir face_recognition==1.2.3
RUN pip3 install picamera==1.13
RUN pip3 install imutils==0.4.3
RUN pip3 install pyserial==3.4
RUN pip3 install Pillow==5.4.1

# install tensorflow
WORKDIR /root
RUN git clone https://github.com/PINTO0309/Tensorflow-bin.git
WORKDIR /root/Tensorflow-bin
RUN pip3 install --upgrade setuptools
RUN apt-get install libhdf5-serial-dev
RUN apt-get install libhdf5-dev
RUN mv tensorflow-1.14.0-cp35-cp35m-linux_armv7l.whl tensorflow-1.14.0-cp37-cp37m-linux_armv7l.whl
RUN pip3 install tensorflow-1.14.0-cp37-cp37m-linux_armv7l.whl

WORKDIR /workspace