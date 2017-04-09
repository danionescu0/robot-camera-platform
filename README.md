What is this?

This is the backend of a mobile camera robot.
The robot will stream the video using [UV4l](http://www.linux-projects.org/uv4l/)
The backend won't interfere with the video stream, but instead will controll the robot movements.
The platform will receive commands using mqtt, and will transmit things like battery level and 
infrared senzors around the robot.

Manual Installation

You can skip this if you'll run it with docker-compose

* uv4l streamming: https://www.instructables.com/id/Raspberry-Pi-Video-Streaming/?ALLSTEPS
* python packages: ````pip install.sh -r requirements.txt````
* mosquitto 3.1: ````sudo apt-get install.sh mosquitto````
* create the empty password file: "/etc/mosquitto/pwfile"
* configure username/password for mosquitto: "mosquitto_passwd -b /etc/mosquitto/pwfile username password"

Docker installation

````
cd ./docker-container
docker-compose build 
docker-compose up
````

Run

* start image streaming: 
````
chmod +x uv4l/install.sh
chmod +x uv4l/start.sh
sh uv4l/start.sh
````

* start the python motor controll server:
```` python server.py ````

How does it work

This server listens commands on mqtt, and forwards them on serial port, 
and vice-versa listens on serial and forward them on mqtt