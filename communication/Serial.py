import serial

class Serial():
    MESSAGE_TERMINATOR = ';'

    def __init__(self, endpoint):
        self.__endpoint = endpoint
        self.__message_buffer = ''
        self.__serial = None

    def connect(self, receive_message_callback):
        self.__serial = serial.Serial(self.__endpoint['port'], self.__endpoint['baud_rate'], timeout=0.5)
        self.__receive_message_callback = receive_message_callback

    def disconnect(self):
        self.__serial.close()

    def send(self, value):
        self.__serial.write(value)

    def listen(self):
        received_data = self.__serial.read()
        print("_"+ received_data.decode() + "_")
        if received_data.decode() == False or received_data.decode() == '':
            return
        self.__message_buffer += received_data.decode()
        if not self.__is_full_message_recived():
            return
        self.__receive_message_callback(self.__message_buffer)
        self.__message_buffer = ''

    def __get_endpoint(self):
        return self.__endpoint

    def __is_full_message_recived(self):
        return True if self.__message_buffer[-1] == self.MESSAGE_TERMINATOR else False
