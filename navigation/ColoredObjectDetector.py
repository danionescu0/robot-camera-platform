import cv2

from navigation.ObjectDetector import ObjectDetector


class ColoredObjectDetector(ObjectDetector):
    def __init__(self, hsv_bounds):
        self.__hsv_bounds = hsv_bounds
        super().__init__()

    def process(self, image):
        self.detected = False
        hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, self.__hsv_bounds[0], self.__hsv_bounds[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) == 0:
            return
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        M = cv2.moments(largest_contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        self.circle_coordonates = (center, int(radius))
        self.detected = True