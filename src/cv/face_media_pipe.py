import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
face_detection = mp.solutions.face_detection.FaceDetection(model_selection=0)

while True:
    ret, frame = cap.read()
    results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.detections:
        for detection in results.detections:
            print("Yuz aniqlandi!")

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
