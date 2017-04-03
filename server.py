import config
import argparse
from time import sleep
from communication.MqttConnection import MqttConnection
from communication.Serial import Serial
from bridge.RobotIO import RobotIO

parser = argparse.ArgumentParser(description='Controlls robot')
parser.add_argument('--debug', dest='debug', action='store_true')
parser.set_defaults(feature=False)
args = parser.parse_args()
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
serial = Serial(config.serial)

robot_io = RobotIO(mqtt_connection, serial, args.debug)
mqtt_connection.connect(robot_io.received_command)
serial.connect(robot_io.received_serial_message)
mqtt_connection.listen()

while True:
    serial.listen()
    sleep(0.05)