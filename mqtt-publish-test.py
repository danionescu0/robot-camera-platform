import paho.mqtt.client as mqtt

client = mqtt.Client()
client.username_pw_set('user', 'Abecedar01')

client.connect("localhost", 1883, 60)
client.loop_start()
client.publish("robot/status", "fwd:2:3", 2)
client.loop_stop()
client.disconnect()