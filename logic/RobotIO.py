from communication.MqttConnection import MqttConnection

class RobotIO:
    COMMUNICATION_TERMINATOR = ';'

    def __init__(self, mqtt_connection, serial, debug):
        self.__mqtt_connection = mqtt_connection
        self.__serial = serial
        self.__debug = debug

    def received_serial_message(self, message):
        print("Sending:" + message)
        self.__mqtt_connection.send(MqttConnection.STATUS_CHANNEL, message)

    def received_command(self, message):
        print("Received command: " + message)
        if not self.__debug:
            self.__serial.send(message + self.COMMUNICATION_TERMINATOR)
