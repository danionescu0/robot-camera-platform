from typing import Callable
import codecs

import paho.mqtt.client as mqtt


class MqttConnection():
    MOVEMENT_CHANNEL = 'robot/movement'
    STATUS_CHANNEL = 'robot/status'

    def __init__(self, host : str, port : str, user : str, password : str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__callback = None
        self.__client = None

    def connect(self):
        self.__client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            self.__client.subscribe(self.MOVEMENT_CHANNEL)

        def on_message(client, userdata, msg):
            if self.__callback is not None:
                self.__callback(msg.payload)

        self.__client.on_connect = on_connect
        self.__client.on_message = on_message
        self.__client.username_pw_set(self.__user, self.__password)
        self.__client.connect_async(self.__host, self.__port, 60)
        self.__client.loop_start()

    def listen(self, callback: Callable[[codecs.StreamReader], None]):
        self.__callback = callback

    def send(self, channel : str, message : str):
        self.__client.publish(channel, message, 2)