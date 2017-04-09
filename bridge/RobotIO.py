import codecs
import logging
from communication.MqttConnection import MqttConnection
from communication.Serial import Serial

class RobotIO:
    COMMUNICATION_TERMINATOR = ';'

    def __init__(self, mqtt_connection : MqttConnection, serial: Serial, logging: logging.Logger):
        self.__mqtt_connection = mqtt_connection
        self.__serial = serial
        self.__logging = logging

    def received_serial_message(self, message: str):
        self.__logging.debug("Received through serial:" + message)
        self.__mqtt_connection.send(MqttConnection.STATUS_CHANNEL, message)

    def received_command(self, message: codecs.StreamReader):
        self.__logging.debug("Received through MQTT: " + message.decode())
        forward_serial = message + self.COMMUNICATION_TERMINATOR.encode()
        self.__serial.send(forward_serial)
