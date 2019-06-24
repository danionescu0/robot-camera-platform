import time

from flask import Flask, Response, request

import config
from communication.Serial import Serial
from navigation.RobotSerialCommandsConverter import RobotSerialCommandsConverter


app = Flask(__name__)
serial = Serial(config.serial['port'], config.serial['baud_rate'])
serial.connect()
commands_converter = RobotSerialCommandsConverter()


@app.route("/api/motors", methods=["POST"])
# this is a naive implementation, will be refactored in the final release
def motors_command():
    request_params = request.form
    command = request_params['command']
    duration = int(request_params['duration'])
    forward = True
    if command == 'left':
        angle = 0
    elif command == 'forward':
        angle = 90
    elif command == 'backwards':
        angle = 90
        forward = False
    else:
        angle = 180
    robot_command = commands_converter.get_steer_command(angle, 80, forward)
    start = int(round(time.time() * 1000))
    while int(round(time.time() * 1000)) - start < duration:
        print (time.time() - start)
        time.sleep(0.1)
        serial.send(robot_command.encode())

    return Response('', status=200, mimetype='application/json')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)