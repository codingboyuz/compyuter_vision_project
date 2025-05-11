import cv2
import face_recognition
import os

# 📁 Ma'lum yuzlar joylashgan papka
KNOWN_FACES_DIR = "known_faces"
known_encodings = []
known_names = []

# 📥 Papkadagi har bir rasmni o‘qib, yuzni enkod qilish
for filename in os.listdir(KNOWN_FACES_DIR):
    image_path = os.path.join(KNOWN_FACES_DIR, filename)
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)

    if encoding:
        known_encodings.append(encoding[0])
        name = os.path.splitext(filename)[0]
        known_names.append(name)

# 🎥 Kamerani ishga tushirish
cap = cv2.VideoCapture('video/1.mp4')

while True:
    ret, frame = cap.read()

    # Yuzlarni topish
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            matched_idx = matches.index(True)
            name = known_names[matched_idx]

        # Ekranga ismni chiqarish
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

