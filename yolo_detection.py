import cv2
import numpy as np
import face_recognition
import time
from ultralytics import YOLO

def yolo_detection():
    # YOLOv10 modelini yuklash
    model = YOLO("yolov10n.pt")

    # Ma'lum insonning yuz encodingini yuklash
    known_image = face_recognition.load_image_file("known_faces/1.png")
    known_encoding = face_recognition.face_encodings(known_image)[0]

    # Video ochish (kamera yoki video fayl)
    cap = cv2.VideoCapture('video/1.mp4')

    # FPS cheklash uchun vaqt belgilash
    fps_limit = 10
    prev_time = 0

    # Frame sanagich
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # FPS limit tekshiruvi
        current_time = time.time()
        if current_time - prev_time < 1 / fps_limit:
            continue
        prev_time = current_time

        frame_count += 1

        # YOLO bilan yuz aniqlash
        results = model(frame)
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                if cls_id == 0:  # 0 = yuz
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    face_img = frame[y1:y2, x1:x2]

                    label = "Noma'lum"
                    color = (0, 0, 255)

                    # Har 5-frame'da tanib olishni bajarish
                    if frame_count % 5 == 0 and face_img.size > 0:
                        try:
                            rgb_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                            encodings = face_recognition.face_encodings(rgb_face)
                            if encodings:
                                match = face_recognition.compare_faces([known_encoding], encodings[0], tolerance=0.5)
                                if match[0]:
                                    label = "Izlanayotgan Inson"
                                    color = (0, 255, 0)
                        except Exception as e:
                            print("Tanib olishda xatolik:", e)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("YOLO + Face Recognition", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    yolo_detection()
