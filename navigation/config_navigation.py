# minimum and maximum HSV touples for color object detector
# the color below is green
# to modify "hsv_bounds" [Here](https://github.com/jrosebr1/imutils/blob/master/bin/range-detector) is a python helper for HSV range detection
hsv_bounds = (
    (46, 83, 0),
    (85, 255, 212)
)

# minimum and maximum object size in percent of image width to be considered a valid detection
object_size_threshold = (4, 80)

#image is resized by width before processing to increase performance (speed)
#increasing "resize_image_by_width" will result in more accurate detection but slower processing
resize_image_by_width = 450

# angle to rotate camera in degreeds
rotate_camera_by = 180