import threading
from datetime import time

import cv2
import face_recognition
from onvif import ONVIFCamera


class OnvifService:
    def __init__(self, ip: str, port: int, user_name: str, password: str):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.password = password

    def get_rest_url(self) -> str:
        camera = ONVIFCamera(self.ip, self.port, self.user_name, self.password)

        media_service = camera.create_media_service()
        profiles = media_service.GetProfiles()
        profile = profiles[0]
        stream_setup = media_service.create_type('GetStreamUri')
        stream_setup.StreamSetup = {
            'Stream': 'RTP-Unicast',
            'Transport': {'Protocol': 'RTSP'}
        }
        stream_setup.ProfileToken = profile.token

        uri_response = media_service.GetStreamUri(stream_setup)
        return uri_response.Uri


# o = OnvifService(ip='192.168.1.136',port=80,user_name="admin",password="123456")
# o.get_rest_url()


import cv2
import face_recognition
import threading
import time
import os


import cv2
import face_recognition
import time
import os


class CameraDetection:
    def __init__(self, source: str):
        """
        :param source: RTSP URL yoki video fayl yo'li
        """
        self.source = source
        self.known_encodings = []
        self.known_names = []
        self.frame_counter = 0

    def load_known_faces(self, known_faces_dir: str):
        """
        Papkadan ma'lum yuzlarni yuklab olish
        :param known_faces_dir: papka manzili
        """
        for filename in os.listdir(known_faces_dir):
            filepath = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(filepath)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.known_encodings.append(encodings[0])
                self.known_names.append(os.path.splitext(filename)[0])
        print(f"{len(self.known_names)} ta ma'lum yuz yuklandi.")

    def start_detection(self):
        """
        Video oqimini ishga tushuradi va yuzlarni aniqlaydi (bitta patokda)
        """
        cap = cv2.VideoCapture(self.source)

        if not cap.isOpened():
            print("Video oqimi ochilmadi!")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame= cv2.resize(frame,(640,360))

            start_time = time.time()
            self.frame_counter += 1

            # Kichiklashtirish va RGB formatga o'tkazish
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Yuzlarni aniqlash va encoding olish
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_encodings, encoding, tolerance=0.5)
                name = "Noma'lum"

                face_distances = face_recognition.face_distance(self.known_encodings, encoding)
                if len(face_distances) > 0:
                    best_match_index = face_distances.argmin()
                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]

                face_names.append(name)

            # Aniqlangan yuzlarni frame ga chizish (koordinatalar kattalashtiriladi)
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                color = (0, 255, 0) if name != "Noma'lum" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # FPS hisoblash
            end_time = time.time()
            fps = 1 / (end_time - start_time) if (end_time - start_time) > 0 else 0
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)


            cv2.imshow('Face Recognition (Single Thread)', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    o = OnvifService(ip='192.168.1.136', port=80, user_name="admin", password="123456")
    rtsp_url = o.get_rest_url()

    cam = CameraDetection(source=rtsp_url)  # Bu yerga RTSP yoki video fayl yo'lini kiriting
    cam.load_known_faces('../../assets/known_faces')
    cam.start_detection()

