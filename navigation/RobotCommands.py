from navigation.MathUtils import MathUtils


class RobotCommands:
    POWER_LIMITS = {'forward' : {'max' : 50, 'min' : 0}, 'backward' : {'max' : -50, 'min' : 0}}
    DIRECTION_LIMITS = {'right' : 50, 'left' : -50}
    MOTOR_COMMAND = 'M:{0}:{1}'
    LIGHT_COMMAND = 'L:{0}'
    MAX_ANGLE = 180
    MIN_ANGLE = 0

    def get_steer_command(self, angle: int, percent_power: int, forward: bool) -> str:
        direction = self.__get_converted_direction(angle)
        power = self.__get_converted_power(percent_power, forward)

        return self.MOTOR_COMMAND.format(direction, power)

    def get_switch_lights_command(self, state: bool) -> str:
        literal_state = {True: '1', False: '0'}

        return self.LIGHT_COMMAND.format(literal_state[state])

    def __get_converted_power(self, percent_power: int, forward: bool) -> str:
        power_limits_key = {True: 'forward', False: 'backward'}[forward]

        return str(MathUtils.remap(
                percent_power, 0, 100,
                self.POWER_LIMITS[power_limits_key]['min'], self.POWER_LIMITS[power_limits_key]['max']))

    def __get_converted_direction(self, angle: int) -> int:
        return MathUtils.remap(angle, self.MIN_ANGLE, self.MAX_ANGLE,
                               self.DIRECTION_LIMITS['left'], self.DIRECTION_LIMITS['right'])