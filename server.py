import config
import argparse
import sys
from LoggingConfig import LoggingConfig

from time import sleep
from communication.MqttConnection import MqttConnection
from communication.Serial import Serial
from bridge.RobotIO import RobotIO

parser = argparse.ArgumentParser(description='Controlls robot')
parser.add_argument('--debug', dest='debug', action='store_true')
parser.set_defaults(feature=False)
args = parser.parse_args()

logging_config = LoggingConfig(config.logging['log_file'], config.logging['log_entries'])
logging_config.enable_debug(args.debug)
logger = logging_config.get_logger()
sys.excepthook = logging_config.set_error_hadler

mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
serial = Serial(config.serial)

robot_io = RobotIO(mqtt_connection, serial, logger)
mqtt_connection.connect(robot_io.received_command)
serial.connect(robot_io.received_serial_message)
mqtt_connection.listen()

while True:
    serial.listen()
    sleep(0.05)