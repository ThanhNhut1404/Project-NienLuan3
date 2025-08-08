from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import re

# Màu sắc
PRIMARY_COLOR = "#2C387E"
BUTTON_COLOR = "#3F51B5"
TEXT_COLOR = "#000000"
HINT_TEXT_COLOR = [0.5, 0.5, 0.5, 1]  # Màu xám nhạt cho gợi ý
BUTTON_COLOR_RGBA = "#303F9F"

# Font và kiểu
FONT_TITLE = "H5"
FONT_NORMAL = "Subtitle1"

# Kích thước
BUTTON_HEIGHT = 56
PADDING = 20
SPACING = 10  # Giảm spacing để nội dung sát nhau hơn

class EditPasswordScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        main_layout = MDBoxLayout(
            orientation="vertical",
            md_bg_color=[1, 1, 1, 1]
        )

        # Toolbar với nút quay lại
        toolbar = MDTopAppBar(
            title="Đổi mật khẩu",
            left_action_items=[["arrow-left", lambda x: self.go_back(x)]],
            md_bg_color=PRIMARY_COLOR,
            size_hint_y=None,
            height=dp(BUTTON_HEIGHT)
        )
        main_layout.add_widget(toolbar)

        # Nội dung chính, bắt đầu ngay dưới toolbar
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(PADDING), 0, dp(PADDING), dp(PADDING)],  # Chỉ padding hai bên và dưới
            spacing=dp(SPACING),
            size_hint=(0.9, None),
            pos_hint={'center_x': 0.5}  # Căn giữa ngang
        )
        content.bind(minimum_height=content.setter('height'))

        # Trường nhập mật khẩu cũ
        self.old_password = MDTextField(
            hint_text="Mật khẩu cũ",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            font_size=16,
            hint_text_color=HINT_TEXT_COLOR,
            password=True
        )
        content.add_widget(self.old_password)

        # Trường nhập mật khẩu mới
        self.new_password = MDTextField(
            hint_text="Mật khẩu mới",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            font_size=16,
            hint_text_color=HINT_TEXT_COLOR,
            password=True
        )
        content.add_widget(self.new_password)

        # Trường xác nhận mật khẩu mới
        self.confirm_password = MDTextField(
            hint_text="Xác nhận mật khẩu mới",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            font_size=16,
            hint_text_color=HINT_TEXT_COLOR,
            password=True
        )
        content.add_widget(self.confirm_password)

        # Nút lưu
        save_button = MDRectangleFlatButton(
            text="Lưu",
            font_style=FONT_NORMAL,
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            md_bg_color=BUTTON_COLOR_RGBA,
            line_color=TEXT_COLOR,
            text_color=TEXT_COLOR
        )
        save_button.bind(on_release=self.save_password)
        content.add_widget(save_button)

        main_layout.add_widget(content)
        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = "setting"

    def save_password(self, instance):
        old_password = self.old_password.text
        new_password = self.new_password.text
        confirm_password = self.confirm_password.text

        # Kiểm tra cơ bản
        if not old_password or not new_password or not confirm_password:
            self.show_dialog("Lỗi", "Vui lòng điền đầy đủ các trường!")
            return
        if new_password != confirm_password:
            self.show_dialog("Lỗi", "Mật khẩu mới và xác nhận không khớp!")
            return
        if len(new_password) < 9:
            self.show_dialog("Lỗi", "Mật khẩu mới phải có ít nhất 9 ký tự!")
            return
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)", new_password):
            self.show_dialog("Lỗi", "Mật khẩu mới phải chứa chữ hoa, chữ thường và số!")
            return

        # Logic lưu mật khẩu (mô phỏng, cần tích hợp với database)
        print(f"Đổi mật khẩu: Mật khẩu cũ: {old_password}, Mật khẩu mới: {new_password}")
        self.show_dialog("Thành công", "Mật khẩu đã được thay đổi!")
        # Xóa các trường sau khi lưu
        self.old_password.text = ""
        self.new_password.text = ""
        self.confirm_password.text = ""

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="Đóng",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()