FROM generalaardvark/rpi-python35

RUN apt-get update && apt-get install -y git ca-certificates

WORKDIR /root
RUN git clone https://github.com/danionescu0/robot-camera-platform.git
RUN pip install -qr /root/robot-camera-platform/requirements.txt

CMD ["python", "/root/debug/server.py"]