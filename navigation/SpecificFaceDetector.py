import cv2

from navigation.ObjectDetector import ObjectDetector


class SpecificFaceDetector(ObjectDetector):
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__known_face_encodings = None
        self.__specific_face_coordonates = None
        self.__tracker = None
        super().__init__()

    def configure(self):
        import face_recognition
        image = face_recognition.load_image_file(self.__file_path)
        self.__known_face_encodings = [face_recognition.face_encodings(image)[0]]

    def process(self, image):
        self.detected = False
        if self.__specific_face_coordonates is None:
            self.__specific_face_coordonates = self.__get_specific_face(image)
            if self.__specific_face_coordonates is None:
                return
            x, y, x1, y1 = self.__specific_face_coordonates
            self.__tracker = cv2.TrackerKCF_create()
            self.__tracker.init(image, (x, y, (x1 - x), abs(y1 - y)))
            self.circle_coordonates = self.__get_center_radius(self.__specific_face_coordonates)
            self.detected = True
            return

        (success, box) = self.__tracker.update(image)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            self.circle_coordonates = self.__get_center_radius((x, y, x + w, y + h))
            self.detected = True
        else:
            self.__specific_face_coordonates = None

    def __get_specific_face(self, image):
        import face_recognition
        rgb_frame = image[:, :, ::-1]
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # for each face found try to match against known faces
            matches = face_recognition.compare_faces(self.__known_face_encodings, face_encoding)
            if True not in matches:
                return None
            first_match_index = matches.index(True)
            top, right, bottom, left = face_locations[first_match_index]
            return (left, top, right, bottom)

    def __get_center_radius(self, coordonates):
        left, top, right, bottom = coordonates
        center = (int(left + (right - left) / 2), int((top + (bottom - top) / 2)))
        radius = int((bottom - top) / 2)

        return (center, radius)