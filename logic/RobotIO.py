from communication.MqttConnection import MqttConnection

class RobotIO:

    def __init__(self, mqtt_connection):
        self.__mqtt_connection = mqtt_connection

    def received_serial_message(self, message):
        self.__mqtt_connection.send(MqttConnection.STATUS_CHANNEL, message)

    def received_command(self, message):
        print "the command:" + message
