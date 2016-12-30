##What is this?
This is the backend of a mobile camera robot.
The robot will stream the video using [UV4l](http://www.linux-projects.org/uv4l/)
The backend won't interfere with the video stream, but instead will controll the robot movements.
The platform will receive commands using mqtt, and will transmit things like battery level and 
infrared senzors around the robot.

##Installation
* python packages: "pip install -r requirements.txt"
* mosquitto 3.1: "sudo apt-get install mosquitto"
* configure username/password for mosquitto: "mosquitto_passwd -c /etc/mosquitto/pwfile username"
and then enter the password twice whenprompted

##Run
python server.py

##How does it work
This server listens commands on mqtt, and forwards them on serial port, 
and vice-versa listens on serial and forward them on mqtt