# Kerakli kutubxonalarni chaqirish
import cv2  # Kamera va rasm bilan ishlash uchun
import face_recognition  # Yuzni aniqlash va tanib olish uchun
import os  # Fayllar va papkalar bilan ishlash uchun
import flet as ft  # UI yaratish uchun Flet kutubxonasi
import threading  # Fon jarayon (thread) ochish uchun

from src.service.service import FrameConvert

# Yuzlar saqlangan papka
KNOWN_FACES_DIR = "known_faces"

# Ma'lum yuzlarning encoding va ismlari saqlanadi
known_encodings = []
known_names = []

# Papkadan barcha yuzlarni yuklab olish
for filename in os.listdir(KNOWN_FACES_DIR):
    image_path = os.path.join(KNOWN_FACES_DIR, filename)  # Fayl yo‘lini hosil qilish
    image = face_recognition.load_image_file(image_path)  # Rasmni yuklab olish
    encoding = face_recognition.face_encodings(image)  # Yuz encoding (raqamli fingerprint)
    if encoding:
        known_encodings.append(encoding[0])  # Encoding ro‘yxatga qo‘shiladi
        known_names.append(os.path.splitext(filename)[0])  # Fayl nomidan ism ajratiladi

# Kamerani ochish (0 - default kamera)
cap = cv2.VideoCapture(0)
convert = FrameConvert(format='PNG')

# Video oqimini uzatish funksiyasi
def stream_video(img_element):
    while True:
        ret, frame = cap.read()  # Kameradan rasm olish
        if not ret:
            break  # Kamera ishlamayotgan bo‘lsa, to‘xtaydi

        # Rasmni RGB formatga o‘tkazish
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Rasmda yuzlarni aniqlash
        face_locations = face_recognition.face_locations(rgb_frame)

        # Aniqlangan yuzlar uchun encoding olish
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Har bir yuzni solishtirish
        for encoding, location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, encoding)  # Ma’lum yuzlar bilan solishtirish
            name = "Unknown"  # Default nomwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
            if True in matches:
                idx = matches.index(True)  # Mos tushgan indeks
                name = known_names[idx]  # Shu indeksdagi ismni olish

            # Yuz atrofini belgilash va ism yozish
            top, right, bottom, left = location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Yashil to‘rtburchak
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)  # Yuqoriga ism yozish

        # OpenCV frame → PIL Image → base64 → Flet Image
        img_element.src_base64 = convert.convert(frame=frame)  # Flet Image'ga base64 rasmni berish
        img_element.update()  # UI yangilash

# Flet UI boshlanish funksiyasi
def main(page: ft.Page):
    page.title = "Face Recognition UI"  # Oyna sarlavhasi
    img = ft.Image(width=640, height=480)  # Rasm ko‘rsatish uchun komponent
    page.add(img)  # Ekranga qo‘shish

    # Kamera oqimini fon jarayonda ishga tushurish
    threading.Thread(target=stream_video, args=(img,), daemon=True).start()

# Flet ilovasini ishga tushurish
ft.app(target=main)

# pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Frame'ni PIL rasmga aylantirish
# buffer = BytesIO()  # Bo‘sh buffer
# pil_image.save(buffer, format="PNG")  # Rasmni PNG formatda xotiraga saqlash
# img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")  # base64 ga aylantirish