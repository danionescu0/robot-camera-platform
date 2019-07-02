#!/bin/bash

apt-get update && apt-get install -y \
    ca-certificates \
    apt-utils \
    curl \
    build-essential

curl http://www.linux-projects.org/listing/uv4l_repo/lrkey.asc | sudo apt-key add -
echo '[ allow-insecure=yes ] deb http://mirrordirector.raspbian.org/raspbian/ jessie main contrib non-free rpi' > /etc/apt/sources.list
echo '[ allow-insecure=yes ] deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ jessie main' >> /etc/apt/sources.list

apt-get update && apt-get upgrade && apt-get install -y --allow-unauthenticated  \
    uv4l uv4l-raspicam \
    uv4l-raspicam-extras \
    uv4l-server \
    uv4l-uvc \
    uv4l-xscreen \
    uv4l-mjpegstream