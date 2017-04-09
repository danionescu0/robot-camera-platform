**What is this?**

This is the backend of a mobile camera robot.

The robot will stream the video using [UV4l](http://www.linux-projects.org/uv4l/)

The python server will receive commands using mqtt from the android application, and will transmit battery level and 
distance around the robot.

To access the frontend (android app) access this [repository](https://github.com/danionescu0/android-robot-camera)

**Manual Installation**

You can skip this if you'll run it with docker-compose

* uv4l streamming: https://www.instructables.com/id/Raspberry-Pi-Video-Streaming/?ALLSTEPS
* python packages: ````pip install.sh -r requirements.txt````
* mosquitto 3.1: ````sudo apt-get install.sh mosquitto````


**Configuration**

Mosquitto configuration:

* create the empty password file: "/etc/mosquitto/pwfile"
* configure username/password for mosquitto: "mosquitto_passwd -b /etc/mosquitto/pwfile username password"

Uv4l configuration:

* by editing uv4l/start.sh you can configure the following aspects of the video streaming: password,
port, framerate, with, height, rotation and some other minor aspects

Python server:

* edit config.py
* replace password with your own password that you've set on the mosquitto server
* optional you can change the baud rate (default 9600) and don't forget to edit that on the arduino-sketch too

**Running project:**

````
cd ./docker-container
docker-compose build # once to install
docker-compose up
````


**Uv4l streamming:**

Start image streaming: 
````
chmod +x uv4l/install.sh
sh /uv4l/install.sh # once to install
chmod +x uv4l/start.sh
sh uv4l/start.sh
````
Stop streaming
````
sudo pkill uv4l
````

**How does it work**

This server listens to movement and light commands from mqtt (android app) and 
forwards them to serial where will be picked up by the listening arduino to 
command the robot.

Also the script listens to serial port for distance updates (front and back) from the 
sensors, and battery level updates (to be implemented).

**Why does an intermediary arduino layer has to exist and not directly the Pi ?**

* it's more modular, you can reuse the arduino robot in another project without the PI
* for safety, it's cheaper to replace a 3$ arduino pro mini than to replace a Pi (35$)
* an arduino it's not intrerupted by the operating system like the pi is, so it's more 
efficient to implement PWM controlls for the mottors, polling the front and back sensors
a few times per second
* if an error might occur in the python script the robot might run forever draining the
batteries and probably damaging it or catching fire if not supervised, in an arduino sketch
a safeguard it's more reliable because it does not depends on an operating system

**ToDo**

* Implement a battery status updater, maby my monitoring the power consumption for the py and arduino.
By knowing the full power of the battery pack an power estimation would be possible.
Email alerts and system shutdown should be in place when power is critical.
* Full tutorial on the project with both hardware and software
* Single configuration file for senstive settings like passwords, usernames hosts