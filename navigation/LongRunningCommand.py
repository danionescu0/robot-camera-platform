import time
from multiprocessing import Process, Queue

from communication.Serial import Serial


class LongRunningCommand(Process):
    SLEEP_INTERVAL = 0.1

    def __init__(self, serial: Serial, input_queue: Queue, command_max_duration: int):
        Process.__init__(self)
        self.__serial = serial
        self.__input_queue = input_queue
        self.__command_max_duration = command_max_duration
        self.__stop = False
        self.__command_started = 0
        self.__last_command = None

    def run(self):
        while not self.__stop:
            command = self.__get_command()
            time.sleep(self.SLEEP_INTERVAL)
            if command is not None:
                self.__command_started = int(round(time.time() * 1000))
                self.__last_command = command
            if command is None and int(round(time.time() * 1000)) - self.__command_started > self.__command_max_duration:
                continue
            self.__serial.send(self.__last_command.encode())
            print("Sending command:" + self.__last_command)

    def stop_process(self):
        self.__stop = True

    def __get_command(self):
        if not self.__input_queue.empty():
            return self.__input_queue.get(False)
        else:
            return None