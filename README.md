# What is this?

  This is the versatile robot platform. I've gave it a few usecases: 
 
* a surveillence robot for home

* a object follower

* remote controll over alexa echo dot

  This is a research project fun to build and fun to explore and we'll take on the following concepts and technologies:
  
* programming: Computer vision, Python, Arduino (C++), Java for Android, AWS lambda functions
 
* miscelanious: MQTT, Docker, Docker compose, UV4l, linux services

* electronics: Raspberry pi, Arduino, H-Bridge, DC motors, sensors, soldering, building a robot etc



# 1. Surveillence robot usecase

![android-app-screenshot1.jpg](https://github.com/danionescu0/robot-camera-platform/blob/master/resources/android-app-screenshot1.jpg)

# 2. Object follower usecase

![object-follower-example1.png](https://github.com/danionescu0/robot-camera-platform/blob/master/resources/object-follower-example1.png)

# 3. Alexa voice robot commands demo

# 4. Building the robot parts & schameatics


**Workarounds for not having a public ip on your dev board**

* the simplest way is tu use a public proxy like https://ngrok.com/ https://ngrok.com/docs#multiple-tunnels

* you can port forward 1883 and 9090 ports on your router


**Why does an intermediary arduino layer has to exist and not directly the Pi ?**

* it's more modular, you can reuse the arduino robot in another project without the PI
* for safety, it's cheaper to replace a 3$ arduino pro mini than to replace a Pi (35$)
* an arduino it's not intrerupted by the operating system like the pi is, so it's more 
efficient to implement PWM controlls for the mottors, polling the front and back sensors
a few times per second
* if an error might occur in the python script the robot might run forever draining the
batteries and probably damaging it or catching fire if not supervised, in an arduino sketch
a safeguard it's more reliable because it does not depends on an operating system

**Prerequisites**

a. Ensure that your development board has an serial port. If your're using a Raspberry pi please ensure that 
the serial console it's disabled and the port can be used. In the config i've assumed it's on /dev/ttyS0

b. Your board works with a camera. If it's raspberry pi and picamera, ensure the camera is connected and 
enabled through raspi-config.


# 1. The first usecase is a surveillence robot that is controlled using an android interface:**
###############################################################################################

Full tutorial on [instructables](https://www.instructables.com/id/Android-Controlled-Robot-Spy-Camera/)

A video demo is available on [youtube](https://youtu.be/6FrEs4C9D-Y)


**How does it work**

a. The android app shows the uv4l streaming inside a webview. The uv4l process runs on the raspberry pi, captures video input from the camera and streams it. 
It's an awesome tool with many features

b. Using controls inside the android app lights and engines commands are issued to the MQTT server

c. The python server inside the docker container on the raspberry pi listens to MQTT commands and passes them
using serial interface to the arduino board. The arduino board controlls the motors and the lights.

d. The arduino board senses distances in front and back of the robot and sends the data through the serial interface to the 
python server, the python forwards them to the MQTT and they get picked up by the android interface and shown to the user

![flow-diagram.png](https://github.com/danionescu0/robot-camera-platform/blob/master/resources/flow-diagram.png)


**Extra**

The robot will stream the video using [UV4l](http://www.linux-projects.org/uv4l/)

The android application is located in this [repository](https://github.com/danionescu0/android-robot-camera)


**Installation for RaspberryPi**

A complete tutorial about uv4l is found here: https://www.instructables.com/id/Raspberry-Pi-Video-Streaming/?ALLSTEPS



**Clone the project in the home folder:**
````
git clone https://github.com/danionescu0/robot-camera-platform
````
The folder location it's important because in docker-compose.yml the location is hardcoded as: /home/pi/robot-camera-platform:/root/debug
If you need to change the location, please change the value in docker-compose too


**Install Uv4l streamming:**
 
````
chmod +x uv4l/install.sh
chmod +x uv4l/start.sh
sh ./uv4l/install.sh 
````

Warning you'll see warning messages: "The following signatures were invalid" because on latest raspbian 
operating system the uv4l packages are not fully supported.

**Configure the project:**

* by editing uv4l/start.sh you can configure the following aspects of the video streaming: password,
port, framerate, with, height, rotation and some other minor aspects
* edit config.py and replace password with your own password that you've set on the mosquitto server
* edit docker-container/mosquitto/Dockerfile and replace this line with your own user and password for mosquitto
````
RUN mosquitto_passwd -b /etc/mosquitto/pwfile user your_password
````


**Test uv4l installation**

a. Start it:
````
sh ./uv4l/start.sh 
````
b. Test it in the browser at the address: http://your_ip:9090/stream

c. Stop it
````
sudo pkill uv4l
````


**Install docker and docker-compose**

About docker installation: https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/
About docker-compose installation: https://www.berthon.eu/2017/getting-docker-compose-on-raspberry-pi-arm-the-easy-way/


**Auto starting services on reboot/startup**

a. Copy the files from systemctl folder in systemctl folder to /etc/systemd/system/

b. Enable services:
````
sudo systemctl enable robot-camera.service
sudo systemctl enable robot-camera-video.service
````

c. Reboot

d. Optional, check status:
````
sudo systemctl status robot-camera.service
sudo systemctl status robot-camera-video.service
````

**Build and install the Android app**

a. Clone the repository
````
git clone https://github.com/danionescu0/android-robot-camera.git
````

b. Follow the instructions there to configure and build it




# 2. Object follower usecase

The robot is able to follow 

- objects of a specific color (YouTube video [youtube](https://youtu.be/z9qLmHRMCZY))

- a known face 

- a person (YouTube video: https://youtu.be/CLvkD5kB7xk)

Prerequisites:

* Enable VNC on raspberry pi
* Install VNC viewer on your operating system and log in into the pi
* Docker is installed

Details: https://www.raspberrypi.org/documentation/remote-access/vnc/

**Install dependencies**

Install using Docker:
````
sudo docker build -t object-tracking .
# the commands below neets to be run on every login
xhost +local:docker;XSOCK=/tmp/.X11-unix;XAUTH=/tmp/.docker.xauth
```` 

Manual install:

* compile opencv: https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

* use virtualenv to install dependencies, you may need to remove opencv from dependencies list
````
 pip3 install virtualenv
 virtualenv object_follower
 source object_follower/bin/activate
 cd /home/pi/robot-camera-platform/
 pip install -r /home/pi/robot-camera-platform/requirements_object_tracking.txt
````


**Troubleshooting:**

* If the camera module is not working please check [this](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera) official Raspberry pi tutorial first

* I've used opencv to capture the camera image from /dev/video0 so ensure it exists, if not you can try to activate it using:

````
sudo modprobe bcm2835-v4l2
````

**Configuration**

In navigation/config_navigation.py you'll find:
````
# minimum and maximum HSV touples for color object detector
# the color below is green
hsv_bounds = (
    (46, 83, 0),
    (85, 255, 212)
)

# minimum and maximum object size in percent of image width to be considered a valid detection
object_size_threshold = (4, 60)

#image is resized by width before processing to increase performance (speed)
#increasing "resize_image_by_width" will result in more accurate detection but slower processing
resize_image_by_width = 450

# angle to rotate camera in degreeds
rotate_camera_by = 180
````

**Optional run unit tests**

Unit tests are using [nose2](http://nose2.readthedocs.io/en/latest/index.html)

In console run:
````
nose2
````

**Running the colored object detector:**

The colored object detector needs HSV calibration, to get a preview of the HSV bounds, you can use the tool located 
in navigation/visual_hsv_bounds.py like so:


Calibration:
````
sudo docker run --device=/dev/video0 --device=/dev/vchiq --device=/dev/ttyS0 \
-e DISPLAY=$DISPLAY -v $XSOCK:$XSOCK \-v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH \
--volume=$(pwd):/workspace object-tracking python3 navigation/visual_hsv_bounds.py 
````


Actually running the colored object detector

````
python3 object_tracking.py colored-object --show-video 

or with docker

sudo docker run --device=/dev/video0 --device=/dev/vchiq --device=/dev/ttyS0 -e DISPLAY=$DISPLAY -v $XSOCK:$XSOCK -v \
$XAUTH:$XAUTH -e XAUTHORITY=$XAUTH --volume=$(pwd):/workspace object-tracking python3 \
object_tracking.py colored-object --show-video
````

Running the object tracking script with no video output means omitting the --show-video parameter


**Running the face detector:**

* a Raspberry PI 4 is recommended with 2.5A power bank
 
```` 
sudo docker run --device=/dev/video0 --device=/dev/vchiq --device=/dev/ttyS0 \
-e DISPLAY=$DISPLAY -v $XSOCK:$XSOCK \-v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH \
--volume=$(pwd):/workspace object-tracking python3 object_tracking.py \
specific-face --extra_cfg /path_to_a_picture_containing_a_face --show-video 
````

**Running the person detector:**

YouTube video: https://youtu.be/CLvkD5kB7xk

Console command:
````
sudo docker run --device=/dev/video0 --device=/dev/vchiq --device=/dev/ttyS0 -e DISPLAY=$DISPLAY -v $XSOCK:$XSOCK \-v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH --volume=$(pwd):/workspace object-tracking python3 object_tracking.py tf-object-detector --show-video
````

**How does the image detection works ?**

**1. colored object detector**
- First the image is converted to HSV
- Using the function "inRange" HSV ranges are applied to the image (the ranges are defined in the the config)
- Erode and Dilate opencv functions are applied to make the interest zones more clear
- FindContours functon is applied and we select the largest contour (the largest colored object)
- From our selected contour we apply "minEnclosingCircle" and "moments" to get the coordonates of a circle that 
will best enclose our largest colored object 

For the code see "ColoredObjectDetector.py" file

**2. face recognition**

For the face recognition we're using "face_recognition" library to extract our specific face of interst from the image.

The problem is this library is quite slow on a development board even if we scale the image to 300 x 300 it takes more than a second for a detection.
We'll use a new adition to Opencv 3.4 object trackers. These trackers are quite fast but far less accurate than "face_detection" technique

So i'm combining the two detectors to build a compromise between the two. First the "face_recognition" library runs in a different async process,
and when a face is found, it communicates to the faster library the face coordonates. 
The faster method is called "TrackerCSRT_create" from the opencv library and it's able to run syncronious on the pi, processing frame by frame and help guide the robot.

For the code you can start with "SpecificFaceDetector.py" file



# 3. Alexa voice robot commands demo

Still work in progress !

**Prerequisites**
For this you'll need:
 
* Alexa Echo Dot speaker: https://www.amazon.com/All-new-Echo-Dot-3rd-Gen/dp/B0792KTHKJ

* The Android / IOS application (check out this guide for pair: https://www.techradar.com/how-to/amazon-echo-setup)

* A developer amazon account and an AWS account: https://developer.amazon.com and https://console.aws.amazon.com

* A ngrok account: https://ngrok.com/ or public ip address


**Configure ngrok**

* Login, download ngrok for Linux (arm) and unzip on the board: https://dashboard.ngrok.com/get-started

* Connect your account running the command, replacing your token with the actual token 
````
./ngrok authtoken your_token
````

* Run the ngrok server on 8080
````
./ngrok http 8080
````

* Create new Skil with the skil from alexa/skil.json, build the skil

* Create new lambda function skil/lambda_function.py , connect it with the skil

* Replace API_ENDPOINT with ngrok instance or your own public ip

* Install dependencies

````
 virtualenv voice_commands
 source voice_commands/bin/activate
 cd /home/pi/robot-camera-platform/
 pip install -r /home/pi/robot-camera-platform/requirements_voice_commands.txt
```` 

* Run the server

````
 source voice_commands/bin/activate
 cd /home/pi/robot-camera-platform/
 python voice_commands.py
````



# 4. Building the robot platform

The arduino sketch can be found in ./arduino-sketck folder.


**Components**

Fritzing schematic:

![fritzig_sketch.png](https://github.com/danionescu0/robot-camera-platform/blob/master/arduino-sketch/sketch_small.png)

**Checklist:** 

- The robot itself, either build it your selves or buy a kit (search TS100 robot tank on ebay, aliexpress)

The important thing to remember is that, the robot should have two DC (6-12V) motors and that each motor should 
be responsable for direction on left respectively right.  

- Small nuts and bolts, spacers

- A robot case, this should be made out of a light material, and it will house the electronics and batteries

- LED light (optional)

- Arduino pro mini 328p 

- 2 x infrared obstacle sensor (optional)

- PCB

- NPN tranzistor (for the flashlight)

- L7805CV 5V regulator

- L298 H-bridge 

- Rezistor 220 Ohms

- Male usb connector, wires

- AMS1117 3.3v regulator (for communication between arduino and raspberry pi)

- Male & female PCB connectors

- On / off switch (for cutting the power to the motor battery)

- 2S 1300 mAh LiPo battery with XT-60 connector, XT-60 female LiPo connector 

- 5v battery pack for the Rasberry

- Raspberry Pi, 16 GB SD card Raspberry Pi card, acrylic case with fan

- Raspberry Pi camera


**Pinout:**

Led flashlight: D3

Left motor: PWM (D5), EN1, EN2(A4, A5)

Right motor: PWM (D6), EN1, EN2(A3, A2)

Infrared sensors: Front (A0), Back(A1)

Serial communication pins: Tx: D11, Rx: D10
