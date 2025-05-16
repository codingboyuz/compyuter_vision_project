import base64  # Rasmni base64 formatga o‘tkazish uchun
from io import BytesIO  # Rasmni xotirada vaqtincha saqlash uchun

import cv2
from PIL import Image  # Rasmni PNG formatga o‘tkazish uchun (Pillow kutubxonasi)

import os
import face_recognition



class FrameConvert:
    def __init__(self, format):
        self.format = format


    def convert(self,frame):
        # BGR -> RGB convert
        rgb_image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # PIL Image ga o'tkazish
        pil_image = Image.fromarray(rgb_image)
        # Bufferga yozib saqlash
        buffer  = BytesIO()

        pil_image.save(buffer,format=self.format)
        img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_b64



class KnownFacesLoader:
    def __init__(self, known_faces_dir):
        self.known_faces_dir = known_faces_dir
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def load_known_faces(self):
        self.known_encodings = []
        self.known_names = []

        for filename in os.listdir(self.known_faces_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.known_faces_dir, filename)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    self.known_encodings.append(encodings[0])
                    # Fayl nomidan kengaytmasiz ism olish
                    self.known_names.append(os.path.splitext(filename)[0])

    def get_encodings(self):
        return self.known_encodings

    def get_names(self):
        return self.known_names
