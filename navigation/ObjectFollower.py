from navigation.MathUtils import MathUtils
from navigation.ObjectDetector import ObjectDetector
from navigation.RobotSerialCommandsConverter import RobotSerialCommandsConverter
from communication.Serial import Serial


class ObjectFollower:
    __MIN_SPEED_PERCENT = 20
    __MAX_SPEED_PERCENT = 33

    def __init__(self, object_detector: ObjectDetector, robot_commands: RobotSerialCommandsConverter,
                 object_size_threshold) -> None:
        self.__object_detector = object_detector
        self.__robot_commands = robot_commands
        self.__object_size_threshold = object_size_threshold
        self.radius = 0
        self.center = (0, 0)
        self.__image = None

    def process(self, image):
        self.__object_detector.process(image)
        self.__image = image
        if self.__object_detector.detected:
            self.center, self.radius = self.__object_detector.circle_coordonates

        return self

    def has_command(self) -> bool:
        if self.radius == 0 or not self.__is_detection_in_range():
            return False

        return True

    def get_command(self) -> str:
        if not self.has_command():
            return None

        return self.__robot_commands.get_steer_command(
                    self.__get_angle(self.center, self.__image),
                    self.__get_speed_percent(self.radius, self.__image),
                    True) +\
               Serial.MESSAGE_TERMINATOR

    def __is_detection_in_range(self):
        height, width, channels = self.__image.shape
        minimum_object_size, maximum_object_size = self.__get_object_bounded_sizes(width)
        if 2 * self.radius >= minimum_object_size and self.radius * 2 <= maximum_object_size:
            return True

        return False

    def __get_object_bounded_sizes(self, actual_object_width):
        return int(self.__object_size_threshold[0] * actual_object_width / 100), \
               int(self.__object_size_threshold[1] * actual_object_width / 100)

    def __get_angle(self, center: tuple, image):
        height, width, channels = image.shape
        x_coordonate = center[0]

        return MathUtils.remap(x_coordonate, 0, width, RobotSerialCommandsConverter.MIN_ANGLE, RobotSerialCommandsConverter.MAX_ANGLE)

    def __get_speed_percent(self, radius, image):
        height, width, channels = image.shape
        minimum_object_size, maximum_object_size = self.__get_object_bounded_sizes(width)

        return MathUtils.remap(radius * 2, minimum_object_size, maximum_object_size,
                               self.__MAX_SPEED_PERCENT, self.__MIN_SPEED_PERCENT)
