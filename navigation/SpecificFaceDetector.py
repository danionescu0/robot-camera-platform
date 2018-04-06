import time

from navigation.ObjectDetector import ObjectDetector


class SpecificFaceDetector(ObjectDetector):
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__known_face_encodings = None

    def configure(self):
        import face_recognition
        image = face_recognition.load_image_file(self.__file_path)
        self.__known_face_encodings = [
            face_recognition.face_encodings(image)[0]
        ]

    def find(self, image):
        import face_recognition
        rgb_frame = image[:, :, ::-1]
        # Find all the faces and face encodings in the current frame of video
        t0 = int(round(time.time() * 1000))
        face_locations = face_recognition.face_locations(rgb_frame)
        t1 = int(round(time.time() * 1000))

        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        t2 = int(round(time.time() * 1000))

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.__known_face_encodings, face_encoding)
            t3 = int(round(time.time() * 1000))
            print(matches, t1-t0, t2-t1, t3-t2)
            # If a match was found in known_face_encodings, just use the first one.
            if True not in matches:
                return (False, False)
            first_match_index = matches.index(True)

            return self.__get_center_radius(face_locations[first_match_index])

        return (False, False)

    def __get_center_radius(self, matched_parameters):
        top, right, bottom, left = matched_parameters
        center = (left + int((right - left) / 2), int(top + (bottom - top) / 2))
        radius = int((bottom -top) / 2)

        return (center, radius)