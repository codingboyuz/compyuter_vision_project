# import cv2
# import face_recognition
# import time
#
# def face_detection_only():
#     known_image = face_recognition.load_image_file('../../assets/known_faces/Dmitriy.png')
#     known_encoding = face_recognition.face_encodings(known_image)[0]
#
#     cap = cv2.VideoCapture('../../assets/vid.mp4')
#
#     frame_counter = 0  # Frame sanagich
#     face_locations = []
#     face_names = []
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         start_time = time.time()
#
#         frame_counter += 1
#
#         # Kichiklashtirish
#         small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
#         rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
#
#         # Har 5-frame da yuzni aniqlash
#         if frame_counter % 1 == 0:
#             face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
#             face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#
#             face_names = []
#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.5)
#                 name = "Noma'lum"
#                 if True in matches:
#                     name = "Izlanayotgan Inson"
#                 face_names.append(name)
#
#         # Chizish
#         for (top, right, bottom, left), name in zip(face_locations, face_names):
#             top *= 2
#             right *= 2
#             bottom *= 2
#             left *= 2
#             color = (0, 255, 0) if name != "Noma'lum" else (0, 0, 255)
#             cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#             cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
#
#         # FPS hisoblash
#         end_time = time.time()
#         delta_time = end_time - start_time
#         fps = 1 / delta_time if delta_time > 0 else 0
#
#         cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
#
#         cv2.imshow('Face Recognition Only', frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
# if __name__ == '__main__':
#     face_detection_only()



import cv2
import face_recognition
import time
import threading

from src.service.onvif_service import OnvifService

face_locations = []
face_names = []
frame_counter = 0
lock = threading.Lock()

def recognize_faces(frame, known_encoding):
    global face_locations, face_names

    # Kichiklashtirish
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    encodings = face_recognition.face_encodings(rgb_small_frame, locations)

    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces([known_encoding], encoding, tolerance=0.5)
        name = "Noma'lum"
        if True in matches:
            name = "Izlanayotgan Inson"
        names.append(name)

    # Global o'zgaruvchilarni yangilash
    with lock:
        face_locations = [(top * 2, right * 2, bottom * 2, left * 2) for (top, right, bottom, left) in locations]
        face_names = names

def face_detection_only():
    global frame_counter

    known_image = face_recognition.load_image_file('../../assets/known_faces/111111111.jpg')
    known_encoding = face_recognition.face_encodings(known_image)[0]

    o = OnvifService(ip='192.168.1.136',port=80,user_name="admin",password="123456")
    r= o.get_rest_url()
    cap = cv2.VideoCapture(r)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 380))  # <== bu yerda aniqlikni pasaytirasiz

        start_time = time.time()
        frame_counter += 1

        # Har 5-frame'da fon patokda yuzni aniqlash
        if frame_counter % 3 == 0:
            threading.Thread(target=recognize_faces, args=(frame.copy(), known_encoding), daemon=True).start()

        # Chizish (oxirgi aniqlangan qiymatlar asosida)
        with lock:
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                color = (0, 255, 0) if name != "Noma'lum" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow('Face Recognition (Threaded)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    face_detection_only()
