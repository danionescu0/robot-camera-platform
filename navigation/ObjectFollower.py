# from typing import Tuple
from navigation.MathUtils import MathUtils
from navigation.ObjectDetector import ObjectDetector
from navigation.RobotCommands import RobotCommands

class ObjectFollower:
    def __init__(self, object_detector: ObjectDetector, robot_commands: RobotCommands,
                 object_size_threshold) -> None:
        self.__object_detector = object_detector
        self.__robot_commands = robot_commands
        self.__object_size_threshold = object_size_threshold

    def get_command(self, image) -> str:
        center, radius = self.__object_detector.find(image)
        if not self.__is_detection_in_range(radius):
            return None
        angle = self.__get_angle(center, image)

        return self.__robot_commands.steer(angle, 30, True)

    def __is_detection_in_range(self, radius):
        if radius >= self.__object_size_threshold[0] and radius <= self.__object_size_threshold[1]:
            return True

        return False

    def __get_angle(self, center, image):
        height, width, channels = image.shape
        x_coordonate = center[0]

        return MathUtils.remap(x_coordonate, 0, width, RobotCommands.MIN_ANGLE, RobotCommands.MAX_ANGLE)
