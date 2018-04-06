import time

import cv2


class FrameProvider:
    def __init__(self, process_image_delay_ms: int) -> None:
        self.__process_image_delay_ms = process_image_delay_ms
        self.__video_capture = None
        self.__last_run = None

    def start(self):
        self.__video_capture = cv2.VideoCapture(0)  # start video capture from raspberry pi camera
        self.__last_run = self.__get_current_millis()

    def stop(self):
        self.__video_capture.release()

    def received_stop(self):
        return cv2.waitKey(30) & 0xFF == ord('q')

    def get_frame(self):
        ret, frame = self.__video_capture.read()
        if ret is not True:
            raise Exception("Video frame not available from opencv")

        return frame

    def has_frame(self):
        current_millis = self.__get_current_millis()
        if current_millis - self.__last_run < self.__process_image_delay_ms:
            return False

        self.__last_run = current_millis

        return True

    def __get_current_millis(self):
        return int(round(time.time() * 1000))