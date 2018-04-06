import cv2

from navigation import config_navigation


class ImageDebug:
    def __init__(self, color, line_width) -> None:
        self.__color = color
        self.__line_width = line_width

    # draws a circle on image to visually mark the object
    # draws the direction on which the robot will move
    def draw_guidelines(self, image, center, radius):
        cv2.circle(image, center, radius, self.__color, self.__line_width)
        height, _, _ = image.shape
        draw_line_distance_from_top = int(height * 0.05)
        cv2.line(image,
            (self.__get_direction_starting_point(center, 0), draw_line_distance_from_top),
            (int(config_navigation.resize_image_by_width / 2), draw_line_distance_from_top),
            self.__color, self.__line_width
        )
        cv2.line(image,
             (self.__get_direction_starting_point(center, 7), draw_line_distance_from_top + 5),
             (self.__get_direction_starting_point(center, 0), draw_line_distance_from_top),
             self.__color, self.__line_width
        )
        cv2.line(image,
             (self.__get_direction_starting_point(center, 7), draw_line_distance_from_top - 5),
             (self.__get_direction_starting_point(center, 0), draw_line_distance_from_top),
             self.__color, self.__line_width
        )

    def __get_direction_starting_point(self, center, add_pixels_to_direction):
        width_middlepoint = int(config_navigation.resize_image_by_width / 2)
        half_distance_from_middlepoint_to_center = int(abs(center[0] - width_middlepoint) / 2)
        if center[0] < width_middlepoint:
            return center[0] + half_distance_from_middlepoint_to_center + add_pixels_to_direction
        else:
            return center[0] - half_distance_from_middlepoint_to_center - add_pixels_to_direction