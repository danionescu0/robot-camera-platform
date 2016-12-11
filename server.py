import config
from communication.MqttConnection import MqttConnection
from communication.Serial import Serial
from logic.RobotIO import RobotIO

def the_callback(data):
    print "incomming motor commands:" + data

mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
serial = Serial(config.serial)

robot_io = RobotIO(mqtt_connection)
mqtt_connection.connect(robot_io.received_command)
serial.connect(robot_io.received_serial_message)

while True:
    mqtt_connection.listen()
    serial.listen()