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
Agar siz **bir vaqtning o‘zida 200 ta IP kameradan** kelayotgan malumotni **aniqlash** ni amalga oshirmoqchi bo‘lsangiz, bu juda katta resurs talab qiladigan va samarali ishlash uchun optimallashtirishni talab qiladigan vazifadir. Quyida **texnik yechimlar** va **optimallashtirish usullari**ni keltiraman.

### 📌 Boshqa tizimlar bilan solishtirganda:

200 ta IP kameradan kelgan oqimlarni real vaqtda kuzatish uchun tizimingiz juda kuchli bo‘lishi kerak. **GPU**, **paralel ishlash**, va **ma'lumotlarni optimal uzatish** juda muhim.

---

## 1. **Tizim Talablari**

### **CPU / GPU**:

* **GPU (NVIDIA RTX 2080/3090)** yoki **NVIDIA Tesla V100/A100** (serverda)
* **CPU**: Kamida **Intel Xeon** yoki **AMD Ryzen Threadripper** (12 yoki undan ko‘p yadroli, yuqori soat chastotasi bilan)
* **RAM**: **64 GB yoki undan yuqori**
* **SSD**: Tez yozish va o‘qish uchun (odatda kameralar uchun 200 oqim katta hajmda bo‘ladi)

### **Tarmoq (Networking)**:

* 200 ta kameraning barcha video oqimlarini qayta ishlash uchun yuqori tezlikda tarmoq kerak bo‘ladi:

  * **Gigabit Ethernet** (yoki undan yuqori, `10GbE` tarmog‘i)
  * **RTSP** oqimlarini uzatish uchun past kechikishlar talab etiladi
  * Kameralar bilan uzatiladigan ma'lumotni yaxshilash uchun **UDP protokoli**ni qo‘llash

---

## 2. **Parallel ishlash (Multithreading / Multiprocessing)**

### **Multithreading yoki Multiprocessing**:

* **Alohida oqimlar** (threads) yoki **protsesslar** har bir kamera uchun yaratilsin.
* Har bir kamera uchun alohida thread yoki process yaratish, video oqimlarini parallelda qayta ishlashni ta'minlaydi.

#### **Multithreading**:

* **GIL (Global Interpreter Lock)** sababli Python’da tarmoqli ishlashda ba'zi cheklovlar bo‘lishi mumkin, lekin u CPU og‘ir yuklarni talab qilmasdan, bir nechta kamera oqimini samarali boshqarishga yordam beradi.

#### **Multiprocessing**:

* Har bir kamera uchun alohida **protsesslar** yaratish orqali resurslarni samarali taqsimlash mumkin.
* Bu usulda har bir kamera uchun **yuklama (CPU)** mustaqil ravishda ishlaydi va tasvirlarni qayta ishlash uchun alohida **protsesslar**ga ega bo‘ladi.

---

## 3. **Optimallashtirish va GPU Qo‘llash**

Agar GPU mavjud bo‘lsa, uni **DeepFace** yoki **YOLO** kabi **model**ga ulangan holda ishlatish mumkin. GPU modelni optimallashtirish uchun ishlatiladi, bu esa juda ko‘p kameralarni qayta ishlashni osonlashtiradi.

* **TensorFlow yoki PyTorch** yordamida **GPU’ni qo‘llab-quvvatlaydigan** modellarni o‘rnatish mumkin.

---

## 4. **Ma'lumotlarni uzatish va saqlash**

* Har bir kameraning oqimi hajmi juda katta bo‘lishi mumkin, shuning uchun:

  * Oqimlarni **videolarni vaqtincha saqlash** uchun SSD diskka yozish.
  * **Cloud yoki distributed computing** yechimlarini (AWS EC2, Google Cloud, Azure) ishlatish orqali yengillashtirish mumkin.
* **Kafka** yoki **RabbitMQ** kabi **asynchronous messaging** tizimlari orqali oqimlarni uzatishni boshqarish mumkin. Bu tizimlar **yukni** tezda qayta ishlashga yordam beradi.

---

## 5. **Kod Misoli**

### 🎯 1. **Multiprocessing + YOLO yoki DeepFace**:

Ko‘p kamerani bir vaqtning o‘zida kuzatish uchun **multiprocessing**ni ishlatish mumkin. Har bir kamera uchun alohida `process` yaratamiz.

```python
import cv2
import numpy as np
from deepface import DeepFace
from multiprocessing import Process

# YOLO modelini yoki DeepFace modelini yuklash
def process_camera_stream(camera_url, model):
    cap = cv2.VideoCapture(camera_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # DeepFace bilan yuzni tanib olish
        result = DeepFace.verify(img1_path="known_faces/1.png", img2_path=frame, enforce_detection=False)
        label = "Izlanayotgan inson" if result["verified"] else "Boshqa inson"
        
        # Ekranda ko‘rsatish
        cv2.putText(frame, label, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow(f"Camera - {camera_url}", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()

# Bir nechta kamera URL'lari
camera_urls = [
    "rtsp://192.168.1.1:554/stream",
    "rtsp://192.168.1.2:554/stream",
    # 200 ta kamerani qo‘shing
]

# Har bir kamera uchun multiprocessingni boshlash
def start_multiple_cameras():
    processes = []
    for url in camera_urls:
        p = Process(target=process_camera_stream, args=(url, 'DeepFace'))
        p.start()
        processes.append(p)

    # Barcha jarayonlarni kutish
    for p in processes:
        p.join()

if __name__ == "__main__":
    start_multiple_cameras()
```

### 🎯 2. **Paralel Video oqimi uchun YOLO (yuzni aniqlash)**:

Agar **YOLO** modelidan foydalansangiz, har bir kamera uchun **multiprocessing** yordamida yuz aniqlashni amalga oshirishingiz mumkin.

```python
from ultralytics import YOLO
from multiprocessing import Process

# YOLO modelini yuklash
model = YOLO("yolov10n.pt")

def process_camera_stream(camera_url):
    cap = cv2.VideoCapture(camera_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO bilan yuzni aniqlash
        results = model(frame)
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                if cls_id == 0:  # Yuzni aniqlash
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, "Yuz", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow(f"Camera - {camera_url}", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()

def start_multiple_cameras():
    processes = []
    camera_urls = [
        "rtsp://192.168.1.1:554/stream",
        "rtsp://192.168.1.2:554/stream",
        # 200 ta kamera
    ]
    for url in camera_urls:
        p = Process(target=process_camera_stream, args=(url,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == "__main__":
    start_multiple_cameras()
```

---

## 6. **Cloud yoki Serverga Yordam**

Agar lokal tizimda barcha kameralarni kuzatish qiyin bo‘lsa:

* **Cloud** xizmatlarini (AWS EC2, Google Cloud) ishlatish mumkin. **Elastic Load Balancer** va **distributed computing** yordamida kameralar oqimini yuklashni taqsimlash.
* **Kubernetes** yordamida kameralarning har bir oqimi uchun alohida konteyner yaratish.

---

## Xulosa

* **Paralel ishlash**: 200 ta IP kamerani boshqarish uchun **multiprocessing** yoki **multi-threading** usulini qo‘llash zarur.
* **GPU qo‘llash**: Agar GPU mavjud bo‘lsa, **DeepFace** yoki **YOLO** kabi modelni GPU'da ishlatish va videoni tezda qayta ishlash mumkin.
* **Cloud yechimlari**: Yangi tizimda ko‘p kameralar uchun yuklamani taqsimlash va tarmoqni optimallashtirish uchun **cloud** yoki **distributed computing** yechimlarini ishlatish mumkin.

Agar yanada aniqroq ko‘rsatmalar yoki texnik yordam kerak bo‘lsa, men yordam berishga tayyorman!
