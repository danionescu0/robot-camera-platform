# from typing import Tuple
from navigation.MathUtils import MathUtils
from navigation.ObjectDetector import ObjectDetector
from navigation.RobotCommands import RobotCommands

class ObjectFollower:
    SPEED = 30

    def __init__(self, object_detector: ObjectDetector, robot_commands: RobotCommands,
                 object_size_threshold) -> None:
        self.__object_detector = object_detector
        self.__robot_commands = robot_commands
        self.__object_size_threshold = object_size_threshold
        self.__radius = 0
        self.__center = (False, False)
        self.__image = None

    def process(self, image):
        self.__center, self.__radius = self.__object_detector.find(image)
        self.__image = image

        return self

    def get_command(self) -> str:
        if self.__center == False or not self.__is_detection_in_range():
            return None
        angle = self.__get_angle(self.__center, self.__image)

        return self.__robot_commands.steer(angle, self.SPEED, self.__get_direction())

    def get_center(self):
        return self.__center

    def get_radius(self):
        return self.__radius

    def __is_detection_in_range(self):
        height, width, channels = self.__image.shape
        minimum_object_size = int(self.__object_size_threshold[0] * width / 100)
        maximum_object_size = int(self.__object_size_threshold[1] * width / 100)
        if 2 * self.__radius >= minimum_object_size and self.__radius * 2 <= maximum_object_size:
            return True

        return False

    def __get_direction(self):
        height, width, channels = self.__image.shape
        maximum_object_size = int(self.__object_size_threshold[1] * width / 100)
        all_most_maximum_object_size = int(0.8 * self.__object_size_threshold[1] * width / 100)
        print(all_most_maximum_object_size, maximum_object_size)
        if 2 * self.__radius >= all_most_maximum_object_size and 2 * self.__radius <= maximum_object_size:
            return False

        return True

    def __get_angle(self, center, image):
        height, width, channels = image.shape
        x_coordonate = center[0]

        return MathUtils.remap(x_coordonate, 0, width, RobotCommands.MIN_ANGLE, RobotCommands.MAX_ANGLE)
