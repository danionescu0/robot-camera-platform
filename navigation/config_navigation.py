# minimum and maximum HSV touples for color object detector
# the color below is green
# to modify "hsv_bounds" use navigation/visual_hsv_bounds.py see README.md for more details
hsv_bounds = (
    (46, 83, 0),
    (85, 255, 212)
)

# tensorflow lite model files
tensorflow_model = {
    'file': './resources/tensorflow/detect.tflite',
    'labels': './resources/tensorflow/coco_labels.txt'
}

# minimum and maximum object size in percent of image width to be considered a valid detection
object_size_threshold = (4, 80)

# minimum and maximum speed percents
# the  mimimum speed percent will be the first touple value, the maximum , the second touple value
speed_limit_percents = (70, 93)

#image is resized by width before processing to increase performance (speed)
#increasing "resize_image_by_width" will result in more accurate detection but slower processing
resize_image_by_width = 450

# angle to rotate camera in degreeds
# change this if your image is upside down or tilted
rotate_camera_by = 0