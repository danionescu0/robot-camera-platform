import time


class Timer:
    def __init__(self) -> None:
        self.__moments = {}

    def count(self, name: str):
        self.__moments[name] = int(time.time() * 1000)

    def end_count(self, name: str) -> int:
        return int(time.time() * 1000) - self.__moments[name]

    def end_count_with_output(self, name: str):
        print(name + ': ' + str(self.end_count(name)))