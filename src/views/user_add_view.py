import os.path
import shutil

import flet as ft


class UserAddView:
    def __init__(self, page: ft.Page):
        self.page = page

        self.first_name = ft.TextField(label="Ism")
        self.last_name = ft.TextField(label="Familya")
        self.middle_name = ft.TextField(label="Otasining ismi")

        self.image = ft.Image(src="assets/images/1.jpg", width=200, height=200,
                              fit=ft.ImageFit.CONTAIN, )  # Tanlangan rasimni uida ko'rsatish
        self.file_picker = ft.FilePicker(on_result=self.__on_file_picked)  # faylni tanlashga o'tish
        self.page.overlay.append(self.file_picker)
        self.dlg_modal = None,  # Alterdialog view uchun

        self.selected_image_path = None  # Tanlangan rasim yo'lini saqalsh

        # Dialogni sahifaga biriktirish
        self.page.dialog = self.dlg_modal

    def __validate(self):
        # Validatsiyadan o'tqazish
        is_valid = True

        if not self.first_name.value:
            self.first_name.error_text = "Ism to‘ldirilishi kerak!"
            is_valid = False
        else:
            self.first_name.error_text = None

        if not self.last_name.value:
            self.last_name.error_text = "Familya to‘ldirilishi kerak!"
            is_valid = False
        else:
            self.last_name.error_text = None

        if not self.middle_name.value:
            self.middle_name.error_text = "Otasining ismi to‘ldirilishi kerak!"
            is_valid = False
        else:
            self.middle_name.error_text = None

        self.__update()
        return is_valid

    def __update(self):
        self.first_name.update()
        self.last_name.update()
        self.middle_name.update()

    def __clear(self):
        # Barcha Fiealdlarni tozalash va default holatga keltirish uchun
        self.first_name.value = ""
        self.last_name.value = ""
        self.middle_name.value = ""
        self.image.src = "assets/images/1.jpg"

    def __on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_image_path = e.files[0].path  # Faqat manzilni saqlaymiz
            self.image.src = self.selected_image_path
            # rasim yuklanganda ui da ko'rinishi uchun image fieldini update qilamiz
            self.image.update()
            print(f"Tanlangan rasm: {self.selected_image_path}")

    def __copy_file(self):
        ext = os.path.splitext(self.selected_image_path)[1]  # .jpg, .png
        # rasim nomini o'zgartirish
        filename = f"{self.last_name.value.strip()}_{self.first_name.value.strip()}{ext}"
        # rasimni keraklo folderga saqalash
        save_path = os.path.join('assets', 'known_faces', filename)

        try:
            # rasimni nusxalash
            shutil.copy(self.selected_image_path, save_path)
            print(f"Rasm saqlandi: {save_path}")
        except Exception as err:
            print(f"Rasm saqlashda xatolik: {err}")

    def __open_file_picker(self, e):
        self.file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)

    def submit(self, e):

        # validatsiyadab o'tsa image tanladi
        if self.__validate():

            # Rasmni saqlash
            if self.selected_image_path:
                # Rasimni biga kerakli foderga nusxalaydi
                self.__copy_file()
            # Fieldlar tozalanadi va UI yangilanib alter dialog yopiladi
            self.__clear()
            self.__update()
            self.__close_dialog(e)
        else:
            print("Validatsiyada xatolik bor!")

    def __view(self):
        self.dlg_modal = ft.AlertDialog(
            # alter dialogdan tashqariga bosin yopilishini o'chirish
            modal=True,
            title=ft.Text("Foydalanuvchi qo‘shish"),
            content=ft.Container(
                width=400,
                height=450,
                content=ft.Column(
                    [
                        # Rasim ustiga bosib rasimni fayldan import qilish
                        # GestureDetector widgetlarni button qili beradi
                        ft.GestureDetector(content=self.image, on_tap=self.__open_file_picker),
                        self.first_name,
                        self.last_name,
                        self.middle_name,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,  # sig‘may qolsa, scroll bo‘ladi
                ),
            ),

            actions=[
                ft.TextButton("Yuborish", on_click=self.submit),
                ft.TextButton("Yopish", on_click=self.__close_dialog)
            ]
        )
        return self.dlg_modal

    # AlterDialog yopish
    def __close_dialog(self, e=None):
        ### AlterDialog yopilishi uchun  open ga Flase berish lozim
        self.dlg_modal.open = False
        # fieldlarni tozalash func
        self.__clear()
        # field larni yangilash olgan qiyatini ui da ko'rinishi uchun
        self.__update()
        # AlterDialog yopilganda ui yangilaydi
        self.page.update()

    # AlterDialog ochish
    def open_dialog(self):
        self.page.open(self.__view())
        self.page.update()
