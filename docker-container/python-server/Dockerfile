FROM generalaardvark/rpi-python35

RUN apt-get update && apt-get install -y git ca-certificates

WORKDIR /root
RUN git clone https://github.com/danionescu0/robot-camera-platform.git
RUN pip install -qr /root/robot-camera-platform/requirements.txt

#for debugging purposes the server runs from the mounted volume /root/debug
#the volume is mounted in docker-compose.yml and it assumes the project is clonned inside /home/pi/robot-camera-platform

CMD ["python", "/root/debug/server.py"]