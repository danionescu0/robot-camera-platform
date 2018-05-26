**What is this?**

  This is the versatile robot platform. I've gave it to possible usecases: a surveillence bot
and a object tracker but there can be more, i'll leave this to your imagination :)


1. Surveillence robot usecase

![android-app-screenshot1.jpg](https://github.com/danionescu0/robot-camera-platform/blob/master/resources/android-app-screenshot1.jpg)

2. Object follower usecase

![object-follower-example1.png](https://github.com/danionescu0/robot-camera-platform/blob/master/resources/object-follower-example1.png)

3. Building the robot parts & schameatics



**1. The first usecase is a surveillence robot that is controlled using an android interface:**
###############################################################################################

Full tutorial on [instructables](https://www.instructables.com/id/Android-Controlled-Robot-Spy-Camera/)

A video demo is available on [youtube](https://youtu.be/6FrEs4C9D-Y)

The robot will stream the video using [UV4l](http://www.linux-projects.org/uv4l/)

The python server will receive commands using mqtt from the android application, and will transmit 
distance in front and behind the robot.

The android application is located in this [repository](https://github.com/danionescu0/android-robot-camera)


**How does it work**

a. The android app shows the uv4l streaming inside a webview. The uv4l process runs on the raspberry pi, captures video input from the camera and streams it. 
It's an awesome tool with many features

b. Using controls inside the android app lights and engines commands are issued to the MQTT server

c. The python server inside the docker container on the raspberry pi listens to MQTT commands and passes them
using serial interface to the arduino board. The arduino board controlls the motors and the lights.

d. The arduino board senses distances in front and back of the robot and sends the data through the serial interface to the 
python server, the python forwards them to the MQTT and they get picked up by the android interface and shown to the user

![flow-diagram.png](https://github.com/danionescu0/robot-camera-platform/blob/master/resources/flow-diagram.png)

**Why does an intermediary arduino layer has to exist and not directly the Pi ?**

* it's more modular, you can reuse the arduino robot in another project without the PI
* for safety, it's cheaper to replace a 3$ arduino pro mini than to replace a Pi (35$)
* an arduino it's not intrerupted by the operating system like the pi is, so it's more 
efficient to implement PWM controlls for the mottors, polling the front and back sensors
a few times per second
* if an error might occur in the python script the robot might run forever draining the
batteries and probably damaging it or catching fire if not supervised, in an arduino sketch
a safeguard it's more reliable because it does not depends on an operating system


**Installation**


*Install Uv4l streamming:*
 
````
chmod +x uv4l/install.sh
chmod +x uv4l/start.sh
sh ./uv4l/install.sh 
````
A complete tutorial about uv4l is found here: https://www.instructables.com/id/Raspberry-Pi-Video-Streaming/?ALLSTEPS



*Clone the project in the home folder:*
````
git clone https://github.com/danionescu0/robot-camera-platform
````
The folder location it's important because in docker-compose.yml the location is hardcoded as: /home/pi/robot-camera-platform:/root/debug
If you need to change the location, please change the value in docker-compose too


*Configuration:*

* by editing uv4l/start.sh you can configure the following aspects of the video streaming: password,
port, framerate, with, height, rotation and some other minor aspects
* edit config.py and replace password with your own password that you've set on the mosquitto server
* edit docker-container/mosquitto/Dockerfile and replace this line
````
RUN mosquitto_passwd -b /etc/mosquitto/pwfile user your_password
````

with your own user and password for mosquitto

* optional you can change the baud rate (default 9600) and don't forget to edit that on the arduino-sketch too


*Test uv4l installation*

a. Start it:
````
sh ./uv4l/start.sh 
````
b. Test it in the browser at the address: http://your_ip:9090/stream

c. Stop it
````
sudo pkill uv4l
````


*Install docker and docker-compose*

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



**2. The second usecase is a object/face following robot**
##########################################################
The robot will follow an object of a specific color color and size threshold.

A demo video is available on [youtube](https://youtu.be/z9qLmHRMCZY)

First install dependencies using pip, the installation process will be quite slow

````
sudo pip3 install -r /home/pi/robot-camera-platform/navigation/requirements.txt
````

*Unit tests*

Unit tests are using [nose2](http://nose2.readthedocs.io/en/latest/index.html)

In console run with:
````
nose2
````

**Troubleshooting:**

* If the camera module is not working please check [this](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera) official Raspberry pi tutorial first

* I've used opencv to capture the camera image from /dev/video0 so ensure it exists, if not you can try to activate it using:

````
sudo modprobe bcm2835-v4l2
````

**Configuration [optional]**

In navigation/config_navigation.py you'll find:
````
# minimum and maximum HSV touples for color object detector
# the color below is green
hsv_bounds = (
    (24, 86, 6),
    (77, 255, 255)
)

# minimum and maximum object size in percent of image width to be considered a valid detection
object_size_threshold = (4, 60)

#image is resized by width before processing to increase performance (speed)
resize_image_by_width = 600

#delay between processing frames, frames are skipped for better performance
process_image_delay_ms = 300

# angle to rotate camera in degreeds
rotate_camera_by = 90
````


[Here](https://github.com/jrosebr1/imutils/blob/master/bin/range-detector) you can find a 
visual HSV object threshold detector.

**Running the project:**

Running the object tracking script in VNC graphical interface in a terminal:
More information of how to install VNC ​[here](https://www.raspberrypi.org/documentation/remote-access/vnc/).

```` python3 object_tracking.py colored-object --show-video ````

This will enable you to view the video, with a circle drawn over it. The circle means 
that the object has been detected.

Running the object tracking script with no video output:

```` python3 object_tracking.py colored-object ````

The face follower it's in alpha state right now, it seems to be very slow.

If you want to give it a try, maby reducing resolution a lot use this:
 
```` python3 object_tracking.py specific-face --extra_cfg /path_to_a_picture_containing_a_face --show-video ````

You can specify other camera source then /dev/video0 by using --camera_device camera_number. If you have more then one
video cameras mounted and you want to user the second /dev/video1 use: --camera_device 1

**3. Building the robot**

First a bit about the hardware. The arduino sketch can be found in arduino-sketck folder.


**Components**

Fritzing schematic:

![fritzig_sketch.png](https://github.com/danionescu0/robot-camera-platform/blob/master/arduino-sketch/sketch_small.png)

**Checklist:** 

1. Plexiglass sheet

2. Plastic sheet ( you can also use a plexiglass sheet here )

3. Glue

4. Tyre + DC motor with gearbox + bracket (eBay) 13$

5. Small nuts and bolts

6. 2 x any directional wheel tyre

7. Small LED flashlight (it will be transformed into a headlight)

8. Arduino pro mini 328p (eBay) 2 $

9. 2 x infrared obstacle sensor

10. PCB

11. NPN tranzistor (to drive the flashlight)

12. L7805CV 5V regulator

13. L298 H-bridge 

14. Rezistor 220 Ohms

15. Male usb connector

16. Male micro usb connector

17. Various wires

18. 3 v regulator (for communication between arduino and raspberry pi)

19. Male & female PCB connectors

20. On / off switch

21. XT-60 female LiPo connector (eBay) 1.2$

22. 2S 1300 mAh LiPo battery with XT-60 connector

23. 5v battery pack

24. Raspberry Pi 3

25. Raspberry Pi card

26. Raspberry Pi case

27. Raspberry Pi camera


**Pinout:**

Led flashlight: D3

Left motor: PWM (D5), EN1, EN2(A4, A5)

Right motor: PWM (D6), EN1, EN2(A3, A2)

Infrared sensors: Front (A0), Back(A1)

Tx: D11, Rx: D10