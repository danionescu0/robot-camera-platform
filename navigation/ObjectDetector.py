import abc


class ObjectDetector(metaclass=abc.ABCMeta):
    def __init__(self):
        self._detected = False
        self._circle_coordonates = None

    @abc.abstractmethod
    def process(self, image):
        pass

    def configure(self):
        pass

    @property
    def detected(self):
        return self._detected

    @property
    def circle_coordonates(self):
        return self._circle_coordonates

    @detected.setter
    def detected(self, value):
        self._detected = value

    @circle_coordonates.setter
    def circle_coordonates(self, value):
        self._circle_coordonates = value