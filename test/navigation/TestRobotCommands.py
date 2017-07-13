import unittest

from navigation.RobotCommands import RobotCommands

class TestRobotCommands(unittest.TestCase):
    def test_steer(self):
        robot_commands = RobotCommands()
        self.assertEqual(robot_commands.steer(0, 0, True), 'M:-50:0')
        self.assertEqual(robot_commands.steer(180, 50, True), 'M:50:25')
        self.assertEqual(robot_commands.steer(90, 50, True), 'M:0:25')
        self.assertEqual(robot_commands.steer(45, 100, True), 'M:-25:50')
        self.assertEqual(robot_commands.steer(45, 100, False), 'M:-25:-50')