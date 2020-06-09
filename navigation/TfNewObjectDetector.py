from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import numpy as np

from PIL import Image
from tflite_runtime.interpreter import Interpreter

from navigation.ObjectDetector import ObjectDetector


class TfNewObjectDetector(ObjectDetector):
    def __init__(self, model_path: str, label_file: str, label: str):
        self.__model_path = model_path
        self.__label_file = label_file
        self.__label = label
        self.__threshold = 0.4
        self.__interpreter = None
        self.__labels = None
        self.__input_width = None
        self.__input_height = None
        super().__init__()

    def configure(self):
        self.__labels = self.__load_labels(self.__label_file)
        self.__interpreter = Interpreter(self.__model_path)
        self.__interpreter.allocate_tensors()
        _, self.__input_height, self.__input_width, _ = self.__interpreter.get_input_details()[0]['shape']

    def process(self, image):
        self.detected = False
        transformed_image = Image.fromarray(image) \
            .convert('RGB') \
            .resize((self.__input_width, self.__input_height), Image.ANTIALIAS)
        results = self.__detect_objects(self.__interpreter, transformed_image, self.__threshold, self.__labels)
        if len(results) > 0:
            left, top, right, bottom = results[0]['bounding_box']
            self.circle_coordonates = self.__get_center_radius((left, top, left + right, top + bottom))
            self.detected = True
        return None

    def __load_labels(self, path):
        """Loads the labels file. Supports files with or without index numbers."""
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = {}
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if len(pair) == 2 and pair[0].strip().isdigit():
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
        return labels

    def __set_input_tensor(self, interpreter, image):
        """Sets the input tensor."""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def __get_output_tensor(self, interpreter, index):
        """Returns the output tensor at the given index."""
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
        return tensor

    def __detect_objects(self, interpreter, image, threshold, labels):
        """Returns a list of detection results, each a dictionary of object info."""
        self.__set_input_tensor(interpreter, image)
        interpreter.invoke()
        # Get all output details
        boxes = self.__get_output_tensor(interpreter, 0)
        classes = self.__get_output_tensor(interpreter, 1)
        scores = self.__get_output_tensor(interpreter, 2)
        count = int(self.__get_output_tensor(interpreter, 3))
        results = []
        for i in range(count):
            if scores[i] >= threshold and labels[classes[i]] == self.__label:
                ymin, xmin, ymax, xmax = boxes[i]
                xmin = int(xmin * self.__input_width)
                xmax = int(xmax * self.__input_width)
                ymin = int(ymin * self.__input_height)
                ymax = int(ymax * self.__input_height)
                result = {
                    'bounding_box': [xmin, ymin, xmax, ymax],
                    'class_id': classes[i],
                    'class_name': labels[classes[i]],
                    'score': scores[i]
                }
                results.append(result)
        return results

    def __get_center_radius(self, coordonates):
        left, top, right, bottom = coordonates
        center = (int(left + (right - left) / 2), int((top + (bottom - top) / 2)))
        radius = int((bottom - top) / 2)
        return (center, radius)