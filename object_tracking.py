import cv2
import imutils

import config
from communication.Serial import Serial
from navigation.ColoredObjectDetector import ColoredObjectDetector
from navigation.RobotCommands import RobotCommands
from navigation.ObjectFollower import ObjectFollower

green_lower = (24, 86, 6)
green_upper = (77, 255, 255)
cap = cv2.VideoCapture(0)

def resize(image, width):
    r = width / image.shape[1]
    dim = (width, int(image.shape[0] * r))

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


serial = Serial(config.serial)
serial.connect(None)
detector = ColoredObjectDetector((green_lower, green_upper))
robot_commands = RobotCommands()
object_follower = ObjectFollower(detector, robot_commands, (10, 100))

while True:
    ret, frame = cap.read()
    if ret == True:
        frame = resize(frame, 600)
        frame = imutils.rotate(frame, 90)
        center, radius = detector.find(frame)
        command = object_follower.get_command(frame)
        if None != command:
            full_command = command + serial.MESSAGE_TERMINATOR
            serial.send(full_command.encode())
            print(command)

        if radius > 10:
            cv2.circle(frame, center, int(radius), (0, 255, 255), 2)
        cv2.imshow('frame', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()