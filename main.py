import flet as ft
import threading
import cv2
import base64
from queue import Queue
import time

from src.cv.cam_onvif import get_rtsp_url  # RTSP URL olish uchun funksiya

class CameraViewer:
    def __init__(self, page: ft.Page):
        self.page = page
        self.frame_queue = Queue()  # Ramkalarni saqlash uchun navbat
        self.image_widget = ft.Image()  # Rasmni ko'rsatish uchun widget
        self.page.add(self.image_widget)

        # ONVIF dan RTSP URL olish (siz oldin qo'lda URL qo'ygan edingiz, endi dinamik)
        ip = '192.168.1.136'
        port = 80
        username = 'admin'
        password = '123456'
        rtsp_url = get_rtsp_url(ip, port, username, password)
        print(f"🎥 RTSP URL: {rtsp_url}")

        # Videoni alohida threadda oqimini boshlaymiz
        threading.Thread(target=self.stream_video, args=(rtsp_url,), daemon=True).start()

        # Har 50 ms da UI yangilanadi
        self.page.update_interval = 50  # ms
        self.page.on_interval = self.update_ui
        self.page.update()

    def stream_video(self, rtsp_url: str):
        cap = cv2.VideoCapture(rtsp_url)
        while True:
            success, frame = cap.read()
            if not success:
                continue
            frame = cv2.resize(frame, (640, 480))
            _, buffer = cv2.imencode(".jpg", frame)
            jpg_as_text = base64.b64encode(buffer).decode("utf-8")

            self.frame_queue.put(jpg_as_text)
            time.sleep(0.03)  # taxminan 30 fps

    def update_ui(self, e):
        if not self.frame_queue.empty():
            frame_data = self.frame_queue.get()
            self.image_widget.src_base64 = frame_data
            self.image_widget.update()

def main(page: ft.Page):
    page.title = "RTSP Kamera Viewer"
    CameraViewer(page)

ft.app(target=main)
