import time
from multiprocessing import Queue

from flask import Flask, Response, request

import config
from communication.Serial import Serial
from navigation.RobotSerialCommandsConverter import RobotSerialCommandsConverter
from voice_commands.CommandsProcess import CommandsProcess

app = Flask(__name__)
serial = Serial(config.serial['port'], config.serial['baud_rate'])
serial.connect()
commands_converter = RobotSerialCommandsConverter()

communication_queue = Queue(maxsize=3)
process = CommandsProcess(serial, communication_queue)
process.daemon = True
process.start()


@app.route("/api/motors", methods=["POST"])
# this is a naive implementation, will be refactored in the final release
def motors_command():
    request_params = request.form
    command = request_params['command']
    angle = 90 if request_params['angle'] == 'None' else int(request_params['angle'])
    if command == 'left':
        angle = 90 - angle
    elif command == 'right':
        angle = 90 + angle
    robot_command = commands_converter.get_steer_command(angle, 80, True)
    print(robot_command)
    communication_queue.put(robot_command, block=False)

    return Response('', status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)