from navigation.ObjectDetector import ObjectDetector
from navigation.ColoredObjectDetector import ColoredObjectDetector
from navigation.SpecificFaceDetector import SpecificFaceDetector
from navigation import config_navigation


class ObjectDetectorFactory:
    @staticmethod
    def get(detector_type: str, extra_configuration) -> ObjectDetector:
        if 'colored-object' == detector_type:
            return ObjectDetectorFactory.__get_colored_object_detector()
        elif 'specific-face' == detector_type:
            return ObjectDetectorFactory.__get_specific_face_detector(extra_configuration)
        else:
            raise Exception('Could not find detector with type: {0} '.format(detector_type))

    @staticmethod
    def __get_colored_object_detector():
        return ColoredObjectDetector(config_navigation.hsv_bounds)

    @staticmethod
    def __get_specific_face_detector(extra_configuration):
        detector = SpecificFaceDetector(extra_configuration)
        detector.configure()

        return detector