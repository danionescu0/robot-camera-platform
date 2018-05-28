import unittest
from unittest.mock import MagicMock
from unittest.mock import PropertyMock

from navigation.ObjectFollower import ObjectFollower
from navigation.RobotSerialCommandsConverter import RobotSerialCommandsConverter
from navigation.ColoredObjectDetector import ColoredObjectDetector


class TestObjectFollower(unittest.TestCase):
    def test_has_command_and_get_command_move_left(self):
        object_detector = self.__get_object_detector(((60, 150), 70))
        robot_commands = self.__get_robot_commands('some_command')
        follower = ObjectFollower(object_detector, robot_commands, (4, 60))

        self.assertFalse(follower.has_command())

        follower.process(self.__get_numpy_image((400, 400, 4)))

        self.assertTrue(follower.has_command())
        self.assertEqual(follower.get_command(), 'some_command;')
        robot_commands.get_steer_command.assert_called_with(27, 25, True)

    def test_get_command_move_right(self):
        object_detector = self.__get_object_detector(((320, 250), 100))
        robot_commands = self.__get_robot_commands('other_command')
        follower = ObjectFollower(object_detector, robot_commands, (4, 60))

        follower.process(self.__get_numpy_image((400, 400, 4)))
        self.assertEqual(follower.get_command(), 'other_command;')

        robot_commands.get_steer_command.assert_called_with(144, 22, True)

    def __get_numpy_image(self, return_shape_value: tuple):
        image = MagicMock()
        type(image).shape = PropertyMock(return_value=return_shape_value)

        return image

    def __get_robot_commands(self, return_value: str):
        robot_commands = RobotSerialCommandsConverter()
        robot_commands.get_steer_command = MagicMock(return_value=return_value)

        return robot_commands

    def __get_object_detector(self, return_value: tuple):
        object_detector = ColoredObjectDetector(((24, 86, 6), (77, 255, 255)))
        object_detector.find = MagicMock(return_value=(return_value))

        return object_detector