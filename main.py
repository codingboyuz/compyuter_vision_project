import threading
from  src.view.user_add_view import UserAddView
import  flet as ft




def main(page: ft.Page):
    page.title = "Add"  # Oyna sarlavhasi
    user_add_view = UserAddView()
    page.add(user_add_view.view())  # Ekranga qo‘shish

    # Kamera oqimini fon jarayonda ishga tushurish
    # threading.Thread(target=stream_video, args=(img,), daemon=True).start()

# Flet ilovasini ishga tushurish

if __name__ == '__main__':

    ft.app(target=main)