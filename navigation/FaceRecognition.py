from navigation.Timer import Timer

class FaceRecognition:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__known_face_encodings = None

    def configure(self):
        import face_recognition
        image = face_recognition.load_image_file(self.__file_path)
        self.__known_face_encodings = [face_recognition.face_encodings(image)[0]]

    def find(self, image):
        import face_recognition
        rgb_frame = image[:, :, ::-1]
        # Find all the faces and face encodings in the current frame of video
        t = Timer()
        t1 = t.count("xx")
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # for each face found try to match against known faces
            matches = face_recognition.compare_faces(self.__known_face_encodings, face_encoding)
            if True not in matches:
                return None
            first_match_index = matches.index(True)
            top, right, bottom, left = face_locations[first_match_index]
            t.end_count_with_output("xx")
            return (left, top, right, bottom)
        return None