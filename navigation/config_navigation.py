# minimum and maximum HSV touples for color object detector
# the color below is green
hsv_bounds = (
    (73, 45, 89),
    (85, 255, 212)
)

# minimum and maximum object size in percent of image width to be considered a valid detection
object_size_threshold = (4, 60)

#image is resized by width before processing to increase performance (speed)
resize_image_by_width = 200

# angle to rotate camera in degreeds
rotate_camera_by = 90