# Face Detection with opencv

### Ishlatilgan kutubxonalar
```python
import cv2
import face_recognition
import os
```

# 📁 Ma'lumlar yuzlar joylashgan papkalari
```python
KNOWN_FACES_DIR = "known_faces"
known_encodings = []
known_names = []
```
# 📥 Papkadagi har bir rasmni o‘qib, yuzni enkod qilish
#### Bu qisimda `KNOWN_FACES_DIR` papkasi ichidagi barcha rasimlarni olib tasivbilan solishtirib chiqadi
```python
for filename in os.listdir(KNOWN_FACES_DIR):
    image_path = os.path.join(KNOWN_FACES_DIR, filename)
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)

    if encoding:
        known_encodings.append(encoding[0])
        name = os.path.splitext(filename)[0]
        known_names.append(name)
```

# 🎥 Kamerani ishga tushirish
```python
# buyerda kamera url si yoki local papkadagi video urls joylanadi
cap = cv2.VideoCapture('video/1.mp4')
```