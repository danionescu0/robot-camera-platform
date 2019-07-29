import cv2
import numpy as np

from navigation.ObjectDetector import ObjectDetector


class TfObjectDetector(ObjectDetector):
    def __init__(self, model_path: str, label_file: str, label: str):
        self.__model_path = model_path
        self.__label_file = label_file
        self.__label = label
        super().__init__()

    def configure(self):
        import tensorflow as tf
        self.__interpreter = tf.lite.Interpreter(model_path=self.__model_path)
        self.__interpreter.allocate_tensors()
        self.__input_details = self.__interpreter.get_input_details()
        self.__output_details = self.__interpreter.get_output_details()
        self.__height = self.__input_details[0]['shape'][1]
        self.__width = self.__input_details[0]['shape'][2]

        with open(self.__label_file, 'r') as f:
            lines = f.readlines()
        self.__labels = {}
        for line in lines:
            pair = line.strip().split(maxsplit=1)
            self.__labels[int(pair[0])] = pair[1].strip()

    def process(self, image):
        floating_model = False
        if self.__input_details[0]['dtype'] == np.float32:
            floating_model = True
        picture = image
        initial_h, initial_w, channels = picture.shape
        frame = cv2.resize(picture, (self.__width, self.__height))
        input_data = np.expand_dims(frame, axis=0)
        if floating_model:
            input_data = (np.float32(input_data) - 127.5) / 127.5
        self.__interpreter.set_num_threads(4)
        self.__interpreter.set_tensor(self.__input_details[0]['index'], input_data)
        self.__interpreter.invoke()
        detected_boxes = self.__interpreter.get_tensor(self.__output_details[0]['index'])
        detected_classes = self.__interpreter.get_tensor(self.__output_details[1]['index'])
        detected_scores = self.__interpreter.get_tensor(self.__output_details[2]['index'])
        num_boxes = self.__interpreter.get_tensor(self.__output_details[3]['index'])
        self.detected = False
        for i in range(int(num_boxes)):
            top, left, bottom, right = detected_boxes[0][i]
            classId = int(detected_classes[0][i])
            score = detected_scores[0][i]
            if self.__label == self.__labels[classId] and score > 0.5:
                self.detected = True
                left = left * initial_w
                bottom = bottom * initial_h
                right = right * initial_w
                top = top * initial_h
                center = (int(left + (right - left) / 2), int((top + (bottom - top) / 2)))
                radius = int((bottom - top) / 2)
                self.circle_coordonates = (center, radius)
                box = [left, top, right, bottom, center, radius]
