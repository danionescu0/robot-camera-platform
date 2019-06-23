import logging
import logging.handlers


class LoggingConfig():
    def __init__(self, filename: str, max_bytes: int):
        self.__filename = filename
        self.__max_bytes = max_bytes
        self.__debug = False

    def enable_debug(self, debug: bool):
        self.__debug = debug

    def get_logger(self) -> logging.Logger:
        formatter = logging.Formatter(fmt='%(levelname)s (%(threadName)-10s) :%(name)s: %(message)s '
                                  '(%(asctime)s; %(filename)s:%(lineno)d)',
                              datefmt="%Y-%m-%d %H:%M:%S")
        handlers = [
            logging.handlers.RotatingFileHandler(self.__filename,
                                                 encoding='utf8',
                                                 maxBytes=self.__max_bytes,
                                                 backupCount=3),
            logging.StreamHandler()
        ]
        self.__root_logger = logging.getLogger()
        if (self.__debug):
            level = logging.DEBUG
        else:
            level = logging.WARNING
        self.__root_logger.setLevel(level)
        for h in handlers:
            h.setFormatter(formatter)
            h.setLevel(level)
            self.__root_logger.addHandler(h)
        return self.__root_logger

    def set_error_hadler(self, type, value, tb):
        self.__root_logger.exception("Uncaught exception: {0}".format(str(value)))