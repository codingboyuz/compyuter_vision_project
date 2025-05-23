import flet as ft

from src.views.user_add_view import UserAddView


class AppBarView:

    def __init__(self, page: ft.Page):
        self.page = page,

        self.add_view = UserAddView(page=page) # User qo'shuvchi AlterDialog oynasini chaqirish

    def view(self):
        return ft.AppBar(
            title=ft.Text("Yuz Aniqlash"),
            bgcolor=ft.Colors.GREEN_50,
            actions=[
                ft.IconButton(icon=ft.Icons.PERSON_ADD, on_click=lambda e: self.add_view.open_dialog()),
                ft.Container(width=20, height=20)

            ]

        )
