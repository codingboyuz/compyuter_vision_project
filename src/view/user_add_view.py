
import flet as ft

class UserAddView:
    def __init__(self):
        self.name_field = ft.TextField(label="Name")
        self.age_field = ft.TextField(label="Age", keyboard_type=ft.KeyboardType.PHONE)
        self.submit_btn = ft.ElevatedButton(text="Submit", on_click=self.submit)

    def submit(self, e):
        name = self.name_field.value
        age = self.age_field.value
        print(f"Name: {name}, Age: {age}")
        # bu yerda siz backendga yuborishingiz yoki validatsiya qilishingiz mumkin

    def view(self):
        return ft.Column(
            [
            self.name_field,
            self.age_field,
            self.submit_btn,
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
