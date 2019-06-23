import serial

from navigation.RobotSerialCommandsConverter import RobotSerialCommandsConverter


class Serial:
    def __init__(self, port: str, baud_rate: str):
        self.__port = port
        self.__baud_rate = baud_rate
        self.__message_buffer = ''
        self.__serial = None
        self.__receive_message_callback = None

    def add_callback(self, receive_message_callback):
        self.__receive_message_callback = receive_message_callback

    def connect(self):
        self.__serial = serial.Serial(self.__port, self.__baud_rate,timeout=0.5, writeTimeout=0.5)

    def disconnect(self):
        self.__serial.close()

    def send(self, value: str):
        self.__serial.write(value)

    def loop(self):
        if self.__receive_message_callback is None:
            return
        received_data = self.__serial.read()
        if received_data.decode() is False or received_data.decode() == '':
            return
        self.__message_buffer += received_data.decode()
        if not self.__has_received_full_message():
            return
        self.__receive_message_callback(self.__message_buffer)
        self.__message_buffer = ''

    def __has_received_full_message(self):
        return True if self.__message_buffer[-1] == RobotSerialCommandsConverter.MESSAGE_TERMINATOR else False
