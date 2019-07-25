from navigation import config_navigation
from navigation.ObjectDetector import ObjectDetector
from navigation.ColoredObjectDetector import ColoredObjectDetector
from navigation.SpecificFaceDetector import SpecificFaceDetector
from navigation.FaceRecognitionProcessWrapper import FaceRecognitionProcessWrapper
from navigation.FaceRecognition import FaceRecognition
from navigation.TfObjectDetector import TfObjectDetector


class ObjectDetectorFactory:
    @staticmethod
    def get(detector_type: str, extra_configuration) -> ObjectDetector:
        if 'colored-object' == detector_type:
            return ObjectDetectorFactory.__get_colored_object_detector()
        elif 'specific-face' == detector_type:
            return ObjectDetectorFactory.__get_specific_face_detector(extra_configuration)
        elif 'tf-object-detector' == detector_type:
            return ObjectDetectorFactory.__get_tf_object_detector()
        else:
            raise Exception('Could not find detector with type: {0} '.format(detector_type))

    @staticmethod
    def __get_colored_object_detector():
        return ColoredObjectDetector(config_navigation.hsv_bounds)

    @staticmethod
    def __get_tf_object_detector():
        # work in progress need to download mobilenet and parametrize it
        tf_object_detector = TfObjectDetector(
            './resources/tflite_for_rpi/mobilenet_v2.tflite',
            './resources/tflite_for_rpi/coco_labels.txt',
            'person'
        )
        tf_object_detector.configure()
        return tf_object_detector

    @staticmethod
    def __get_specific_face_detector(extra_configuration):
        face_recognition = FaceRecognition(extra_configuration)
        face_recognition.configure()
        face_recognition_process_wrapper = FaceRecognitionProcessWrapper(face_recognition, 1)
        face_recognition_process_wrapper.start()
        return SpecificFaceDetector(face_recognition_process_wrapper)