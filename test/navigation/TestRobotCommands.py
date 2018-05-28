import unittest

from navigation.RobotSerialCommandsConverter import RobotSerialCommandsConverter


class TestRobotCommands(unittest.TestCase):
    def test_steer(self):
        robot_commands = RobotSerialCommandsConverter()
        self.assertEqual(robot_commands.get_steer_command(0, 0, True), 'M:-50:0')
        self.assertEqual(robot_commands.get_steer_command(180, 50, True), 'M:50:25')
        self.assertEqual(robot_commands.get_steer_command(90, 50, True), 'M:0:25')
        self.assertEqual(robot_commands.get_steer_command(45, 100, True), 'M:-25:50')
        self.assertEqual(robot_commands.get_steer_command(45, 100, False), 'M:-25:-50')

    def test_light(self):
        robot_commands = RobotSerialCommandsConverter()
        self.assertEqual(robot_commands.get_switch_lights_command(True), 'L:1')
        self.assertEqual(robot_commands.get_switch_lights_command(False), 'L:0')