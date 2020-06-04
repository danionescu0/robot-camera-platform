from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import numpy as np
import picamera
import cv2

from PIL import Image
from tflite_runtime.interpreter import Interpreter

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# add this to requirements.txt https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl; sys_platform == "linux"
# work in progress

def load_labels(path):
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


def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold, labels):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold and labels[classes[i]] == 'person':
      ymin, xmin, ymax, xmax = boxes[i]
      xmin = int(xmin * CAMERA_WIDTH)
      xmax = int(xmax * CAMERA_WIDTH)
      ymin = int(ymin * CAMERA_HEIGHT)
      ymax = int(ymax * CAMERA_HEIGHT)
      result = {
          'bounding_box': [xmin, ymin, xmax, ymax],
          'class_id': classes[i],
          'class_name': labels[classes[i]],
          'score': scores[i]
      }
      results.append(result)
  return results



def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model', help='File path of .tflite file.', required=True)
  parser.add_argument(
      '--labels', help='File path of labels file.', required=True)
  parser.add_argument(
      '--threshold',
      help='Score threshold for detected objects.',
      required=False,
      type=float,
      default=0.4)
  args = parser.parse_args()

  labels = load_labels(args.labels)
  interpreter = Interpreter(args.model)
  interpreter.allocate_tensors()
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

  with picamera.PiCamera(
      resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:
    camera.start_preview()
    try:
      stream = io.BytesIO()
      for _ in camera.capture_continuous(
          stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        image = Image.open(stream).convert('RGB').resize(
            (input_width, input_height), Image.ANTIALIAS)
        results = detect_objects(interpreter, image, args.threshold, labels)
        print(results)
        stream.seek(0)
        stream.truncate()
        # cv2.imshow('frame', stream)

    finally:
      camera.stop_preview()


if __name__ == '__main__':
  main()