import argparse

import cv2
import imutils

import config
from communication.Serial import Serial
from navigation import config_navigation
from navigation.ObjectFollower import ObjectFollower
from navigation.RobotCommands import RobotCommands
from navigation.ObjectDetectorFactory import ObjectDetectorFactory


# configure argument parser
parser = argparse.ArgumentParser(description='Robot configuration')
parser.add_argument(
    'detector_type', action='store',
    help='Select detector type available types: colored-object, specific-face. For '
         'specific face an --extra-cfg is required with an image path containing the face to be followed'
)
parser.add_argument(
    '--extra_cfg', dest='extra_cfg', action='store',
    help='Extra parameter for detector_type'
)
parser.add_argument('--show-video', dest='video', action='store_true', help='shows images on desktop')
parser.set_defaults(feature=False)
args = parser.parse_args()


#configure serial
serial = Serial(config.serial)
serial.connect(None)
detector = ObjectDetectorFactory.get(args.detector_type, args.extra_cfg)
robot_commands = RobotCommands()
object_follower = ObjectFollower(detector, robot_commands, config_navigation.object_size_threshold)
video_capture = cv2.VideoCapture(0) # start video capture from raspberry pi camera

while True:
    ret, frame = video_capture.read()
    if ret is not True:
        break
    frame = imutils.resize(frame, width=600)  # image is resised by with with 600 px for better performance
    frame = imutils.rotate(frame, 90) # image is rotated 90 degreeds due to the robot camera position
    object_follower.process(frame)
    if object_follower.has_command():
        command = object_follower.get_command()
        full_command = command + serial.MESSAGE_TERMINATOR
        serial.send(full_command.encode())
        #draws a circle on image to visually mark the object
        cv2.circle(frame, object_follower.get_center(), int(object_follower.get_radius()), (0, 255, 255), 2)
        print('Motor command: {0}'.format(command))
    if args.video:
        cv2.imshow('frame', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video_capture.release()