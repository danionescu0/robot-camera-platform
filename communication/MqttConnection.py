import paho.mqtt.client as mqtt
from typing import Callable
import codecs

class MqttConnection():
    MOVEMENT_CHANNEL = 'robot/movement'
    STATUS_CHANNEL = 'robot/status'

    def __init__(self, host : str, port : str, user : str, password : str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password

    def connect(self, receive_message_callback: Callable[[codecs.StreamReader], None]):
        self.__receive_message_callback = receive_message_callback
        self.client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            self.client.subscribe(self.MOVEMENT_CHANNEL)

        def on_message(client, userdata, msg):
            self.__receive_message_callback(msg.payload)

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.username_pw_set(self.__user, self.__password)
        self.client.connect_async(self.__host, self.__port, 60)

    def listen(self):
        self.client.loop_start()

    def send(self, channel : str, message : str):
        self.client.publish(channel, message, 2)