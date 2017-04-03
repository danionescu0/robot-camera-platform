FROM generalaardvark/rpi-python35

RUN apt-get update && apt-get install -y git
WORKDIR /root
#RUN git clone https://github.com/danionescu0/robot-camera-platform.git
#COPY config.py /root/robot-camera-platform/
#COPY requirements.txt /root/robot-camera-platform/
RUN mkdir -p /root/robot-camera-platform/
COPY ./robot-camera-platform/   /root/robot-camera-platform/
RUN pip install -qr /root/robot-camera-platform/requirements.txt

CMD ["python", "/root/robot-camera-platform/server.py"]