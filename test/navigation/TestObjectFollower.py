import unittest
from unittest.mock import MagicMock

from navigation.ObjectFollower import ObjectFollower
from navigation.RobotCommands import RobotCommands
from navigation.ColoredObjectDetector import ColoredObjectDetector


class TestObjectFollower(unittest.TestCase):
    def test_get_command_left(self):
        object_detector = ColoredObjectDetector(((24, 86, 6), (77, 255, 255)))
        object_detector.find = MagicMock(return_value=((100, 150), 70))

        robot_commands = RobotCommands()
        robot_commands.get_steer_command = MagicMock(return_value='M:-25:50;')

        object_follower = ObjectFollower(object_detector, robot_commands, (4, 60))
        object_follower.process('someimagecontent')
        object_follower.get_command()

        # object_detector.find('someimagecontent')
        object_detector.find.assert_called_with('someimagecontent')

        # robot_commands.get_steer_command(15, 25, True)
        # robot_commands.get_steer_command.assert_called_with(15, 25, True)
        print('ok')