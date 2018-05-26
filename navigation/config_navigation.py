# minimum and maximum HSV touples for color object detector
# the color below is green
hsv_bounds = (
    (24, 86, 6),
    (77, 255, 255)
)

# minimum and maximum object size in percent of image width to be considered a valid detection
object_size_threshold = (4, 60)

#image is resized by width before processing to increase performance (speed)
resize_image_by_width = 600

#delay between processing frames, frames are skipped for better performance
process_image_delay_ms = 100

# angle to rotate camera in degreeds
rotate_camera_by = 90