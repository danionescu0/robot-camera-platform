import abc


class ObjectDetector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, image):
        pass

    @abc.abstractmethod
    def configure(self):
        pass