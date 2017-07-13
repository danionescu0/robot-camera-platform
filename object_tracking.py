import cv2
import imutils
import argparse

import config
import config_navigation
from communication.Serial import Serial
from navigation.ColoredObjectDetector import ColoredObjectDetector
from navigation.RobotCommands import RobotCommands
from navigation.ObjectFollower import ObjectFollower

parser = argparse.ArgumentParser(description='Display video')
parser.add_argument('--show-video', dest='video', action='store_true')
parser.set_defaults(feature=False)
args = parser.parse_args()

serial = Serial(config.serial)
serial.connect(None)
detector = ColoredObjectDetector(config_navigation.hsv_bounds)
robot_commands = RobotCommands()
object_follower = ObjectFollower(detector, robot_commands, config_navigation.object_size_threshold)

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if ret != True:
        break
    frame = imutils.resize(frame, width=600)
    frame = imutils.rotate(frame, 90)
    command = object_follower.process(frame).get_command()
    if None != command:
        full_command = command + serial.MESSAGE_TERMINATOR
        serial.send(full_command.encode())
        print(command)
    if object_follower.get_radius() != False:
        cv2.circle(frame, object_follower.get_center(), int(object_follower.get_radius()), (0, 255, 255), 2)
    if args.video:
        cv2.imshow('frame', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video_capture.release()