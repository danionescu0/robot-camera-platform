from multiprocessing import Queue

from navigation.FaceRecognitionProcess import FaceRecognitionProcess
from navigation.FaceRecognition import FaceRecognition


class FaceRecognitionProcessWrapper:
    QUEUE_SIZE = 2

    def __init__(self, face_recognition: FaceRecognition, nr_threads: int) -> None:
        self.__face_recognition = face_recognition
        self.__nr_threads = nr_threads
        self.__input_queue = None
        self.__output_queue = None

    def start(self):
        self.__input_queue = Queue(maxsize=self.QUEUE_SIZE)
        self.__output_queue = Queue(maxsize=self.QUEUE_SIZE)
        process = FaceRecognitionProcess(self.__face_recognition, self.__input_queue, self.__output_queue)
        process.daemon = True
        process.start()

    def put_image(self, image):
        self.__empty_input_queue()
        try:
            self.__input_queue.put(image, block=False)
        except:
            pass

    def get_result(self) -> tuple:
        if self.__output_queue.qsize() > 0:
            try:
                return self.__output_queue.get(block=False)
            except:
                return None, None

        return None, None

    def __empty_input_queue(self):
        while not self.__input_queue.empty():
            try:
                self.__input_queue.get(block=False)
            except:
                return