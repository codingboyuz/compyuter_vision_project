from deepface import DeepFace
import cv2

def deep_face_detection():
    # Ma'lum insonning suratini yuklaymiz
    target_img_path = "../../known_faces/1.png"
    target_img = cv2.imread(target_img_path)

    # Kameradan oqim ochamiz
    cap = cv2.VideoCapture('../../video/1.mp4')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.verify(img1_path=target_img, img2_path=frame, enforce_detection=False)
            if result["verified"]:
                label = "Izlanayotgan inson"
                color = (0, 255, 0)
            else:
                label = "Boshqa inson"
                color = (0, 0, 255)

            cv2.putText(frame, label, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        except Exception as e:
            print("Xatolik:", e)

        cv2.imshow("DeepFace - Yuz Tanib Olish", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    deep_face_detection()
