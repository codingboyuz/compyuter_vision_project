import cv2
import mediapipe as mp

from src.cv.cam_onvif import get_rtsp_url


def media_pipe(rtsp_url):
    # Face Mesh moduli
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                      max_num_faces=1,
                                      min_detection_confidence=0.5,
                                      min_tracking_confidence=0.5)

    # Ko‘rsatish uchun chizuvchi
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    # Kamera ochish (0 – kompyuterning webcam, yoki IP kamera manzili)
    cap = cv2.VideoCapture(rtsp_url)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Tasvir olinmadi.")
            break

        # Tasvirni BGR dan RGB ga o‘zgartirish
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Yuz meshini aniqlash
        results = face_mesh.process(image_rgb)

        # Rasmga chizish uchun qayta BGR formatga o‘tkazamiz
        image.flags.writeable = True

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Yuzning 468 nuqtasini chizish
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_spec)

                # Misol: ogʻiz ochiqligini aniqlash
                top_lip = face_landmarks.landmark[13]  # Yuqori lab markeri
                bottom_lip = face_landmarks.landmark[14]  # Pastki lab markeri
                lip_distance = abs(top_lip.y - bottom_lip.y)

                if lip_distance > 0.03:
                    cv2.putText(image, "Ogʻiz ochiq", (30, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Misol: ko‘z ochiqligini aniqlash (chap ko‘z)
                left_eye_top = face_landmarks.landmark[159]
                left_eye_bottom = face_landmarks.landmark[145]
                eye_opening = abs(left_eye_top.y - left_eye_bottom.y)

                if eye_opening < 0.015:
                    cv2.putText(image, "Koʻz yumilgan", (30, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Natijani ko‘rsatish
        image = cv2.resize(image, (1920, 1080))
        cv2.imshow('MediaPipe Face Mesh', image)

        # Chiqarish uchun 'q'
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    ip = '192.168.1.136'
    port = 80
    username = 'admin'
    password = '123456'

    try:
        rtsp_url = get_rtsp_url(ip, port, username, password)
        print(f"🎥 RTSP URL: {rtsp_url}")
        media_pipe(rtsp_url)
    except Exception as e:
        print(e)
