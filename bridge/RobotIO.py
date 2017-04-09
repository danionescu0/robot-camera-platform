import codecs
from communication.MqttConnection import MqttConnection
from communication.Serial import Serial

class RobotIO:
    COMMUNICATION_TERMINATOR = ';'

    def __init__(self, mqtt_connection : MqttConnection, serial: Serial, debug: bool):
        self.__mqtt_connection = mqtt_connection
        self.__serial = serial
        self.__debug = debug

    def received_serial_message(self, message: str):
        print("Received command through serial:" + message)
        self.__mqtt_connection.send(MqttConnection.STATUS_CHANNEL, message)

    def received_command(self, message: codecs.StreamReader):
        print("Received command through MQTT: " + message.decode())
        if not self.__debug:
            forward_serial = message + self.COMMUNICATION_TERMINATOR.encode()
            self.__serial.send(forward_serial)
