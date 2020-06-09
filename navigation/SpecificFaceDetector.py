import cv2

from navigation.ObjectDetector import ObjectDetector
from navigation.FaceRecognitionProcessWrapper import FaceRecognitionProcessWrapper


class SpecificFaceDetector(ObjectDetector):
    def __init__(self, face_recognition: FaceRecognitionProcessWrapper):
        self.__tracker = None
        self.__face_recognition = face_recognition
        super().__init__()

    def process(self, image):
        self.detected = False
        self.__face_recognition.put_image(image)
        original_image, coordonates = self.__face_recognition.get_result()
        if original_image is not None:
            x, y, x1, y1 = coordonates
            if not hasattr(cv2, 'TrackerCSRT_create') or not callable(getattr(cv2, 'TrackerCSRT_create')):
                self.circle_coordonates = self.__get_center_radius((x, y, x1, y1))
                self.detected = True
                return
            self.__tracker = cv2.TrackerCSRT_create()
            self.__tracker.init(original_image, (x, y, (x1 - x), abs(y1 - y)))
            return

        if self.__tracker is None:
            return

        (success, box) = self.__tracker.update(image)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            self.circle_coordonates = self.__get_center_radius((x, y, x + w, y + h))
            self.detected = True

    def __get_center_radius(self, coordonates):
        left, top, right, bottom = coordonates
        center = (int(left + (right - left) / 2), int((top + (bottom - top) / 2)))
        radius = int((bottom - top) / 2)
        return (center, radius)