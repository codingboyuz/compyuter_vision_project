import flet as ft

from src.views.app_bar_view import AppBarView
from src.views.user_add_view import UserAddView


def main(page: ft.Page):
    page.title = "Foydalanuvchi qo‘shish dialogi"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    app_bar_view = AppBarView(page=page)

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.update()

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.update()

    page.add(
        app_bar_view.view(),
        ft.ElevatedButton("Choose files...",
                          on_click=lambda _: file_picker.pick_files(allow_multiple=True))

    )

ft.app(target=main)

