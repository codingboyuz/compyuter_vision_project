# import flet as ft
#
# from src.views.app_bar_view import AppBarView
# from src.views.user_add_view import UserAddView
#
#
# def main(page: ft.Page):
#     page.title = "Foydalanuvchi qo‘shish dialogi"
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#
#     app_bar_view = AppBarView(page=page)
#
#     file_picker = ft.FilePicker()
#     page.overlay.append(file_picker)
#     page.update()
#
#     file_picker = ft.FilePicker()
#     page.overlay.append(file_picker)
#     page.update()
#
#     page.add(
#         app_bar_view.view(),
#         ft.ElevatedButton("Choose files...",
#                           on_click=lambda _: file_picker.pick_files(allow_multiple=True))
#
#     )
#

# ft.app(target=main)
#
#
#
# import flet as ft
# import cv2
# import face_recognition
# import base64
# import threading
# import os
# from io import BytesIO
# from PIL import Image
#
# class CameraViewer:
#     def __init__(self, page: ft.Page):
#         self.page = page
#         self.page.title = "iVMS Style Camera Viewer"
#         self.cameras = {
#             "Cam 1": "rtsp://admin:Admin2021@192.168.100.114:554/stream1",
#             "Cam 2": "rtsp://admin:Admin2021@192.168.100.125:554/stream1"
#         }
#         self.image_widgets = []
#         self.build()
#
#     def stream_video(image_widget: ft.Image, rtsp_url: str):
#         cap = cv2.VideoCapture(rtsp_url)
#
#         while True:
#             success, frame = cap.read()
#             if not success:
#                 continue
#
#             frame = cv2.resize(frame, (640, 480))
#             _, buffer = cv2.imencode(".jpg", frame)
#             jpg_as_text = base64.b64encode(buffer).decode("utf-8")
#
#             def update_image():
#                 image_widget.src_base64 = jpg_as_text
#                 image_widget.update()
#
#             ft.app(target=lambda p: p.call_later(update_image))  # ishlamasligi mumkin
#
#     def build(self):
#         grid_items = []
#
#         for name, rtsp_url in self.cameras.items():
#             image_widget = ft.Image(
#                 expand=True,
#                 fit=ft.ImageFit.CONTAIN,
#                 error_content=ft.Text("Kamerani ochib bo‘lmadi")
#             )
#             self.image_widgets.append(image_widget)
#
#             threading.Thread(
#                 target=self.stream_video,
#                 args=(image_widget, rtsp_url),
#                 daemon=True
#             ).start()
#
#             grid_items.append(
#                 ft.Draggable(
#                     group="cameras",
#                     content=ft.Container(
#                         content=ft.Column([
#                             ft.Text(name, weight=ft.FontWeight.BOLD),
#                             ft.Container(
#                                 content=image_widget,
#                                 expand=True,
#                                 alignment=ft.alignment.center,
#                                 padding=5,
#                                 border=ft.border.all(1, ft.Colors.GREY),
#                                 border_radius=5
#                             )
#                         ]),
#                         padding=5
#                     )
#                 )
#             )
#
#         # GridView orqali joylash
#         grid = ft.GridView(
#             expand=True,
#             runs_count=2,  # 2 ta ustun
#             max_extent=500,
#             spacing=10,
#             run_spacing=10,
#             child_aspect_ratio=4/3,
#             controls=grid_items
#         )
#
#         self.page.add(grid)
#
# def main(page: ft.Page):
#     viewer = CameraViewer(page)
#
# ft.app(target=main)

#
# import cv2
# import base64
# from PIL import Image
# from io import BytesIO
#
# class FrameConvert:
#     def __init__(self, format="PNG"):
#         self.format = format
#
#     def convert(self, frame):
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image = Image.fromarray(rgb_frame)
#         buffer = BytesIO()
#         image.save(buffer, format=self.format)
#         return base64.b64encode(buffer.getvalue()).decode("utf-8")
#
#
# import os
# import face_recognition
#
# def load_known_faces(directory="assets/known_faces"):
#     encodings = []
#     names = []
#
#     for filename in os.listdir(directory):
#         path = os.path.join(directory, filename)
#         image = face_recognition.load_image_file(path)
#         encoding = face_recognition.face_encodings(image)
#         if encoding:
#             encodings.append(encoding[0])
#             names.append(os.path.splitext(filename)[0])
#
#     return encodings, names
#
#
# import cv2
# import threading
# import flet as ft
# import face_recognition
#
#
#
# class CameraStream:
#     def __init__(self, rtsp_url: str, img_element: ft.Image, known_encodings, known_names):
#         self.rtsp_url = rtsp_url
#         self.img_element = img_element
#         self.known_encodings = known_encodings
#         self.known_names = known_names
#         self.converter = FrameConvert()
#         self.cap = cv2.VideoCapture(rtsp_url)
#         self.running = True
#
#     def start(self):
#         threading.Thread(target=self.__stream_loop, daemon=True).start()
#
#     def __stream_loop(self):
#         while self.running:
#             ret, frame = self.cap.read()
#             if not ret:
#                 continue
#
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             face_locations = face_recognition.face_locations(rgb_frame)
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#             for encoding, location in zip(face_encodings, face_locations):
#                 matches = face_recognition.compare_faces(self.known_encodings, encoding, tolerance=0.6)
#                 name = "Unknown"
#                 if True in matches:
#                     idx = matches.index(True)
#                     name = self.known_names[idx]
#
#                 top, right, bottom, left = location
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
#
#             self.img_element.src_base64 = self.converter.convert(frame)
#             self.img_element.update()
#
#
# class CameraViewer:
#     def __init__(self, camera_urls: list[str]):
#         self.camera_urls = camera_urls
#         self.streams = []
#         self.known_encodings, self.known_names = load_known_faces()
#
#     def build(self):
#         self.image_elements = [
#             ft.Image(
#                 width=1,
#                 height=1,
#                 fit=ft.ImageFit.CONTAIN,
#                 error_content=ft.Text("Stream error")
#             )
#             for _ in self.camera_urls
#         ]
#
#         for i, url in enumerate(self.camera_urls):
#             stream = CameraStream(
#                 rtsp_url=url,
#                 img_element=self.image_elements[i],
#                 known_encodings=self.known_encodings,
#                 known_names=self.known_names
#             )
#             stream.start()
#             self.streams.append(stream)
#
#         # GridView: Avtomatik ekran o‘lchamiga moslashadi
#         return ft.GridView(
#             expand=True,
#             max_extent=400,  # Har bir karta maksimal o‘lchami
#             runs_count=0,
#             child_aspect_ratio=4 / 3,
#             spacing=10,
#             run_spacing=10,
#             controls=self.image_elements
#         )
#
#
# def main(page: ft.Page):
#     page.title = "Ko‘p kamerali yuzni aniqlash"
#     page.window_maximized = True
#     page.scroll = "auto"
#
#     # RTSP URL'laringizni shu ro'yxatga qo'shing
#     camera_urls = [
#         "rtsp://admin:password@192.168.100.10:554/Streaming/Channels/101",
#         "rtsp://admin:password@192.168.100.11:554/Streaming/Channels/101",
#         # Qo‘shimcha kameralar ...
#     ]
#
#     viewer = CameraViewer(camera_urls=camera_urls)
#     page.add(viewer.build())
#
# ft.app(target=main)

import os
import cv2
import threading
import base64
import flet as ft
import face_recognition
from PIL import Image
from io import BytesIO

# === Yuzlar ma'lumotini yuklash ===
def load_known_faces(directory="assets/known_faces"):
    encodings = []
    names = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        image = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            encodings.append(encoding[0])
            names.append(os.path.splitext(filename)[0])
    return encodings, names


# === Ramkani base64 formatga o‘tkazish ===
def convert_frame_to_base64(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    buffer = BytesIO()
    pil_image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# === Kamera oqimini boshqarish ===
class CameraStream:
    def __init__(self, rtsp_url: str, img_element: ft.Image, known_encodings, known_names):
        self.rtsp_url = rtsp_url
        self.img_element = img_element
        self.known_encodings = known_encodings
        self.known_names = known_names
        self.cap = cv2.VideoCapture(rtsp_url)
        self.running = True

    def start(self):
        threading.Thread(target=self.__update_loop, daemon=True).start()

    def __update_loop(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for encoding, location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_encodings, encoding, tolerance=0.6)
                name = "Unknown"
                if True in matches:
                    index = matches.index(True)
                    name = self.known_names[index]

                top, right, bottom, left = location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            self.img_element.src_base64 = convert_frame_to_base64(frame)
            self.img_element.update()


# === Asosiy sahifa ===
def main(page: ft.Page):
    page.title = "RTSP Ko‘p Kamera Yuz Aniqlash"
    page.window_maximized = True
    page.scroll = "auto"

    # 👇 Shu yerga barcha kameralaringizni qo‘shing:
    camera_urls = [
        f"rtsp://admin:(con74ol*)@192.168.1.64:554/Streaming/Channels/{i}01"
        for i in range(1, 101)
        # Yana qo‘shish mumkin...
    ]
    print(f"{camera_urls}\n\n")

    known_encodings, known_names = load_known_faces()

    image_elements = []
    streams = []

    for url in camera_urls:
        img = ft.Image(expand=True, fit=ft.ImageFit.CONTAIN)
        image_elements.append(img)
        stream = CameraStream(
            rtsp_url=url,
            img_element=img,
            known_encodings=known_encodings,
            known_names=known_names
        )
        stream.start()
        streams.append(stream)

    page.add(
        ft.GridView(
            expand=True,
            max_extent=400,
            runs_count=len(camera_urls),
            child_aspect_ratio=4 / 3,
            spacing=10,
            run_spacing=10,
            controls=image_elements
        )
    )

ft.app(target=main)
