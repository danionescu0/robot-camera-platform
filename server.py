import config
import argparse
import sys
from LoggingConfig import LoggingConfig

from time import sleep
from communication.MqttConnection import MqttConnection
from communication.Serial import Serial
from bridge.RobotIO import RobotIO


# configure argument parset
parser = argparse.ArgumentParser(description='Controlls robot')
parser.add_argument('--debug', dest='debug', action='store_true')
parser.set_defaults(feature=False)
args = parser.parse_args()

# configure logging and exception handler
logging_config = LoggingConfig(config.logging['log_file'], config.logging['log_entries'])
logging_config.enable_debug(args.debug)
logger = logging_config.get_logger()
sys.excepthook = logging_config.set_error_hadler

# configure mqtt connection, serial and RobotIO bridge
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
serial = Serial(config.serial)

robot_io = RobotIO(mqtt_connection, serial, logger)
mqtt_connection.listen(robot_io.received_command)
mqtt_connection.connect()
serial.add_callback(robot_io.received_serial_message)
serial.connect()


# listen to serial commands in an infinite loop
while True:
    serial.listen()
    sleep(0.05)