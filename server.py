import config
import argparse
import sys
from LoggingConfig import LoggingConfig

from time import sleep
from communication.MqttConnection import MqttConnection
from communication.Serial import Serial
from communication.SerialMqttBridge import SerialMqttBridge


# configure argument parser
parser = argparse.ArgumentParser(description='Controlls robot')
parser.add_argument('--debug', dest='debug', action='store_true')
parser.set_defaults(feature=False)
args = parser.parse_args()

# configure logging and exception handler
logging_config = LoggingConfig(config.logging['log_file'], config.logging['log_entries'])
logging_config.enable_debug(args.debug)
logger = logging_config.get_logger()
sys.excepthook = logging_config.set_error_hadler

# configure mqtt connection, serial and SerialMqttBridge bridge
mqtt_connection = MqttConnection(config.mqtt['host'], config.mqtt['port'], config.mqtt['user'], config.mqtt['password'])
serial = Serial(config.serial['port'], config.serial['baud_rate'])

bridge = SerialMqttBridge(mqtt_connection, serial, logger)
mqtt_connection.listen(bridge.received_command)
mqtt_connection.connect()
serial.add_callback(bridge.received_serial_message)
serial.connect()


# listen to serial commands in an infinite loop
while True:
    serial.loop()
    sleep(0.05)