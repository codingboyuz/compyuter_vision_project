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
        result = DeepFace.verify(img1_path="known_faces/Dmitriy.png", img2_path=frame, enforce_detection=False)
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



---

# Ui qo'lanma rout
Agar sizda bir nechta UI komponentlari (masalan: UserAddView, UserListView, SettingsView, va hokazo) bo‘lsa, ularni sahifaga qo‘shishning bir nechta varianti bor. Quyida har bir yondashuvni tushuntiraman:

---

### 🟢 1. Barchasini bir vaqtning o‘zida sahifaga qo‘shish

Agar barcha UI'lar bir sahifada ko‘rinishini istasangiz:

```python
from src.view.user_add_view import UserAddView
from src.view.user_list_view import UserListView
from src.view.settings_view import SettingsView
import flet as ft

def main(page: ft.Page):
    page.title = "Main Page"

    user_add = UserAddView()
    user_list = UserListView()
    settings = SettingsView()

    page.add(
        user_add.view(),
        user_list.view(),
        settings.view(),
    )

ft.app(target=main)
```

---

### 🔁 2. Faqat bittasini ko‘rsatib, boshqalarini sahifalar (routes) orqali boshqarish

Agar siz `"/add"`, `"/list"`, `"/settings"` kabi yo‘llar (routing) orqali UI'larni boshqarmoqchi bo‘lsangiz:

```python
def main(page: ft.Page):
    page.title = "Main App"

    def route_change(route):
        page.views.clear()

        if page.route == "/add":
            page.views.append(ft.View("/add", controls=[UserAddView().view()]))

        elif page.route == "/list":
            page.views.append(ft.View("/list", controls=[UserListView().view()]))

        elif page.route == "/settings":
            page.views.append(ft.View("/settings", controls=[SettingsView().view()]))

        page.update()

    page.on_route_change = route_change
    page.go("/add")  # Boshlang‘ich sahifa

ft.app(target=main)
```

---

### 📌 3. UI'larni `Tabs`, `NavigationRail`, yoki `Drawer` orqali almashtirish

Agar sahifalar o‘rtasida `Tab` yoki `Drawer` menyu bilan almashmoqchi bo‘lsangiz, masalan:

```python
def main(page: ft.Page):
    def on_change(e):
        index = e.control.selected_index
        if index == 0:
            content.content = UserAddView().view()
        elif index == 1:
            content.content = UserListView().view()
        elif index == 2:
            content.content = SettingsView().view()
        page.update()

    tabs = ft.Tabs(
        selected_index=0,
        on_change=on_change,
        tabs=[
            ft.Tab(text="Add User"),
            ft.Tab(text="User List"),
            ft.Tab(text="Settings"),
        ],
    )

    content = ft.Container(content=UserAddView().view())
    page.add(tabs, content)

ft.app(target=main)
```

---

💬 Qaysi uslub sizga mos? Har birini amaliy tarzda yozib berishim mumkin. Routingmi yoki `Tabs`mi ishlatmoqchisiz?


```python
import cv2
import face_recognition
import threading
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
        self.face_locations = []
        self.face_names = []
        self.lock = threading.Lock()
        self.frame_counter = 0
        self.process_this_frame = True  # Yuzni har 2-frame da bir marta aniqlash uchun flag
        self.running = False

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

    def recognize_faces_in_frame(self, frame):
        """
        Yuzlarni aniqlash va nomlash uchun metod (thread ichida ishlaydi)
        """
        # Kichiklashtirish va RGB formatga o'tkazish
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Yuzlarni aniqlash
        locations = face_recognition.face_locations(rgb_small_frame)
        encodings = face_recognition.face_encodings(rgb_small_frame, locations)

        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(self.known_encodings, encoding, tolerance=0.5)
            name = "Noma'lum"

            face_distances = face_recognition.face_distance(self.known_encodings, encoding)
            if len(face_distances) > 0:
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = self.known_names[best_match_index]

            names.append(name)

        # Natijalarni lock bilan saqlash
        with self.lock:
            self.face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in locations]
            self.face_names = names

    def start_detection(self):
        """
        Video oqimini ishga tushuradi va yuzlarni aniqlaydi
        """
        self.running = True
        cap = cv2.VideoCapture(self.source)

        if not cap.isOpened():
            print("Video oqimi ochilmadi!")
            return

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            self.frame_counter += 1

            # Har 2-frame da bir marta yuzni aniqlash
            if self.frame_counter % 2 == 0:
                # Threadda aniqlash, shunda video oqimi to'xtamaydi
                threading.Thread(target=self.recognize_faces_in_frame, args=(frame.copy(),), daemon=True).start()

            # Chizish uchun oxirgi natijalarni olish
            with self.lock:
                for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                    color = (0, 255, 0) if name != "Noma'lum" else (0, 0, 255)
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # FPS ko'rsatish
            cv2.putText(frame, f"Frame: {self.frame_counter}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

            cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False


if __name__ == "__main__":
    cam = CameraDetection(source='../../assets/vid.mp4')  # Bu yerga RTSP yoki video fayl yo'lini kiriting
    cam.load_known_faces('../../assets/known_faces')
    cam.start_detection()

```