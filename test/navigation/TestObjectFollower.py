import unittest
from unittest.mock import MagicMock
from unittest.mock import PropertyMock

from navigation.ObjectFollower import ObjectFollower
from navigation.RobotSerialCommandsConverter import RobotSerialCommandsConverter
from navigation.ColoredObjectDetector import ColoredObjectDetector


class TestObjectFollower(unittest.TestCase):
    def test_has_command_and_get_command_move_left_fast(self):
        object_detector, robot_commands, follower = self.__get_objects_for_for_left_steer(20)
        self.assertFalse(follower.has_command())

        follower.process(self.__get_numpy_image((400, 400, 4)))

        self.assertTrue(follower.has_command())
        self.assertEqual(follower.get_command(), 'some_command;')
        robot_commands.get_steer_command.assert_called_with(27, 75, True)

    def test_has_command_and_get_command_move_left_slow(self):
        object_detector, robot_commands, follower = self.__get_objects_for_for_left_steer(150)
        follower.process(self.__get_numpy_image((400, 400, 4)))
        self.assertEqual(follower.get_command(), 'some_command;')
        robot_commands.get_steer_command.assert_called_with(27, 23, True)

    def test_get_command_move_right(self):
        object_detector = self.__get_object_detector(True, ((320, 250), 28))
        robot_commands = self.__get_robot_commands('other_command')
        follower = ObjectFollower(object_detector, robot_commands, (4, 60), (20, 80))

        follower.process(self.__get_numpy_image((400, 400, 4)))
        self.assertEqual(follower.get_command(), 'other_command;')

        robot_commands.get_steer_command.assert_called_with(144, 69, True)

    def __get_numpy_image(self, return_shape_value: tuple):
        image = MagicMock()
        type(image).shape = PropertyMock(return_value=return_shape_value)
        return image

    def __get_robot_commands(self, return_value: str):
        robot_commands = RobotSerialCommandsConverter()
        robot_commands.get_steer_command = MagicMock(return_value=return_value)
        return robot_commands

    def __get_object_detector(self, detected: bool, circle_coordonates: tuple):
        object_detector = ColoredObjectDetector(((24, 86, 6), (77, 255, 255)))
        object_detector.process = MagicMock(return_value=(None))
        object_detector.detected = detected
        object_detector.circle_coordonates = circle_coordonates
        return object_detector

    def __get_objects_for_for_left_steer(self, object_size: int):
        object_detector = self.__get_object_detector(True, ((60, 150), object_size))
        robot_commands = self.__get_robot_commands('some_command')
        follower = ObjectFollower(object_detector, robot_commands, (4, 80), (20, 80))
        return object_detector, robot_commands, follower