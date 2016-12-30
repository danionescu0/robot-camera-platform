import config
from time import sleep
from communication.MqttConnection import MqttConnection
from communication.Serial import Serial
from logic.RobotIO import RobotIO

mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
serial = Serial(config.serial)

robot_io = RobotIO(mqtt_connection, serial)
mqtt_connection.connect(robot_io.received_command)
serial.connect(robot_io.received_serial_message)

while True:
    mqtt_connection.listen()
    serial.listen()
    sleep(0.05)