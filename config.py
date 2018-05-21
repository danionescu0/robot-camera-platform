mqtt = {
    'host' : 'mosquitto',
    'port' : 1883, # mosquitto default port
    'user' : 'user',
    'password' : 'your_password'
}

logging = {
    'log_file': '/var/log/robot-camera.txt',
    'log_entries': 20000000
}

serial = {
    'port' : '/dev/ttyS0',
    'baud_rate' : '9600'
}