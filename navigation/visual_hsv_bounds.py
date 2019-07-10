import cv2


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)
    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255
        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, lambda: None)


def get_trackbar_values(range_filter):
    values = []
    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)
    return values


def main():
    camera = cv2.VideoCapture(0)
    setup_trackbars('HSV')
    while True:
        ret, image = camera.read()
        if not ret:
            break
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values('HSV')
        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
        cv2.imshow("Original", image)
        cv2.imshow("Thresh", thresh)
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break


if __name__ == '__main__':
    main()