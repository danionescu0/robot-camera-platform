import imutils

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

    def has_command(self) -> bool:
        if self.__center is False or not self.__is_detection_in_range():
            return False
        return True

    def get_command(self) -> str:
        if not self.has_command():
            return None
        angle = self.__get_angle(self.__center, self.__image)

        return self.__robot_commands.steer(angle, self.SPEED, self.__should_move_forward())

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

    def __should_move_forward(self):
        return True

    def __get_angle(self, center, image):
        height, width, channels = image.shape
        x_coordonate = center[0]

        return MathUtils.remap(x_coordonate, 0, width, RobotCommands.MIN_ANGLE, RobotCommands.MAX_ANGLE)