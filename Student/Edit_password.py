from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.relativelayout import MDRelativeLayout
import re
import sqlite3
import hashlib
from Database.Create_db import update_sinh_vien, get_all_sinh_vien

# Hàm mã hóa mật khẩu bằng sha256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Màu sắc
PRIMARY_COLOR = "#2C387E"
BUTTON_COLOR = "#3F51B5"
TEXT_COLOR = "#000000"
HINT_TEXT_COLOR = [0.5, 0.5, 0.5, 1]
BUTTON_COLOR_RGBA = "#303F9F"
CARD_BG_COLOR = [0.95, 0.95, 0.95, 1]

# Font và kiểu
FONT_TITLE = "H5"
FONT_NORMAL = "Subtitle1"

# Kích thước
BUTTON_HEIGHT = 56
PADDING = 24
SPACING = 16

class EditPasswordScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Giả sử bạn truyền mssv từ phiên đăng nhập
        self.mssv = None  # Thay bằng cách lấy mssv từ session
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        main_layout = MDBoxLayout(
            orientation="vertical",
            md_bg_color=[1, 1, 1, 1]
        )

        # Toolbar
        toolbar = MDTopAppBar(
            title="Đổi mật khẩu",
            left_action_items=[["arrow-left", lambda x: self.go_back(x)]],
            md_bg_color=PRIMARY_COLOR,
            size_hint_y=None,
            height=dp(BUTTON_HEIGHT),
            elevation=2
        )
        main_layout.add_widget(toolbar)

        # ScrollView chứa nội dung
        scroll_view = MDScrollView(
            size_hint=(1, 1)
        )

        # Card chứa các trường nhập liệu
        card = MDCard(
            orientation="vertical",
            padding=dp(PADDING),
            spacing=dp(SPACING),
            size_hint=(1, None),
            height=dp(450),  # Tăng chiều cao để chứa thêm các trường
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=CARD_BG_COLOR,
            elevation=3
        )

        # Trường nhập MSSV
        self.mssv_input = MDTextField(
            hint_text="Mã số sinh viên",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            font_size=16,
            hint_text_color=HINT_TEXT_COLOR,
            line_color_focus=BUTTON_COLOR_RGBA
        )
        card.add_widget(self.mssv_input)

        # Trường nhập mật khẩu cũ
        old_pass_layout = MDRelativeLayout(size_hint_y=None, height=dp(BUTTON_HEIGHT))
        self.old_password = MDTextField(
            hint_text="Mật khẩu cũ",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            font_size=16,
            hint_text_color=HINT_TEXT_COLOR,
            password=True,
            line_color_focus=BUTTON_COLOR_RGBA,
            pos_hint={'center_y': 0.5}
        )
        self.old_eye_button = MDIconButton(
            icon='eye-off',
            pos_hint={'center_y': 0.5, 'right': 1},
            theme_icon_color="Hint",
            on_release=lambda x: self.toggle_password_visibility(self.old_password, self.old_eye_button)
        )
        old_pass_layout.add_widget(self.old_password)
        old_pass_layout.add_widget(self.old_eye_button)
        card.add_widget(old_pass_layout)

        # Trường nhập mật khẩu mới
        new_pass_layout = MDRelativeLayout(size_hint_y=None, height=dp(BUTTON_HEIGHT))
        self.new_password = MDTextField(
            hint_text="Mật khẩu mới",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            font_size=16,
            hint_text_color=HINT_TEXT_COLOR,
            password=True,
            line_color_focus=BUTTON_COLOR_RGBA,
            pos_hint={'center_y': 0.5}
        )
        self.new_eye_button = MDIconButton(
            icon='eye-off',
            pos_hint={'center_y': 0.5, 'right': 1},
            theme_icon_color="Hint",
            on_release=lambda x: self.toggle_password_visibility(self.new_password, self.new_eye_button)
        )
        new_pass_layout.add_widget(self.new_password)
        new_pass_layout.add_widget(self.new_eye_button)
        card.add_widget(new_pass_layout)

        # Trường xác nhận mật khẩu mới
        confirm_pass_layout = MDRelativeLayout(size_hint_y=None, height=dp(BUTTON_HEIGHT))
        self.confirm_password = MDTextField(
            hint_text="Xác nhận mật khẩu mới",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            font_size=16,
            hint_text_color=HINT_TEXT_COLOR,
            password=True,
            line_color_focus=BUTTON_COLOR_RGBA,
            pos_hint={'center_y': 0.5}
        )
        self.confirm_eye_button = MDIconButton(
            icon='eye-off',
            pos_hint={'center_y': 0.5, 'right': 1},
            theme_icon_color="Hint",
            on_release=lambda x: self.toggle_password_visibility(self.confirm_password, self.confirm_eye_button)
        )
        confirm_pass_layout.add_widget(self.confirm_password)
        confirm_pass_layout.add_widget(self.confirm_eye_button)
        card.add_widget(confirm_pass_layout)

        # Nút lưu
        save_button = MDRectangleFlatButton(
            text="Lưu",
            font_style=FONT_NORMAL,
            size_hint=(1, None),
            height=dp(BUTTON_HEIGHT),
            md_bg_color=BUTTON_COLOR_RGBA,
            line_color=TEXT_COLOR,
            text_color=TEXT_COLOR,
            pos_hint={'center_x': 0.5}
        )
        save_button.bind(on_release=self.save_password)
        card.add_widget(save_button)

        scroll_view.add_widget(card)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def toggle_password_visibility(self, text_field, eye_button):
        text_field.password = not text_field.password
        eye_button.icon = 'eye' if not text_field.password else 'eye-off'

    def go_back(self, instance):
        self.manager.current = "setting"

    def save_password(self, instance):
        mssv = self.mssv_input.text.strip()
        old_password = self.old_password.text.strip()
        new_password = self.new_password.text.strip()
        confirm_password = self.confirm_password.text.strip()

        # Kiểm tra cơ bản
        if not mssv or not old_password or not new_password or not confirm_password:
            self.show_dialog("Lỗi", "Vui lòng điền đầy đủ các trường!")
            return
        if new_password != confirm_password:
            self.show_dialog("Lỗi", "Mật khẩu mới và xác nhận không khớp!")
            return
        if len(new_password) < 6:
            self.show_dialog("Lỗi", "Mật khẩu mới phải có ít nhất 6 ký tự!")
            return
        if not re.search(r'[A-Z]', new_password):
            self.show_dialog("Lỗi", "Mật khẩu mới phải chứa ít nhất 1 chữ cái in hoa!")
            return
        if not re.search(r'[a-z]', new_password):
            self.show_dialog("Lỗi", "Mật khẩu mới phải chứa ít nhất 1 chữ cái thường!")
            return
        if not re.search(r'\d', new_password):
            self.show_dialog("Lỗi", "Mật khẩu mới phải chứa ít nhất 1 số!")
            return
        if " " in new_password:
            self.show_dialog("Lỗi", "Mật khẩu mới không được chứa khoảng trắng!")
            return

        try:
            # Tìm sinh viên dựa trên MSSV
            conn = sqlite3.connect('Database/Diem_danh.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM SINH_VIEN WHERE MSSV = ?", (mssv,))
            student_data = cursor.fetchone()

            if not student_data:
                self.show_dialog("Lỗi", "Không tìm thấy sinh viên với MSSV này!")
                conn.close()
                return

            # Lấy mật khẩu hiện tại (PASSWORD_SV là cột thứ 10)
            stored_password = student_data[9]
            print(f"[DEBUG] Stored password: {stored_password}")

            # Kiểm tra mật khẩu cũ
            hashed_old_password = hash_password(old_password)
            print(f"[DEBUG] Hashed old password: {hashed_old_password}")
            if stored_password != hashed_old_password:
                self.show_dialog("Lỗi", "Mật khẩu cũ không đúng!")
                conn.close()
                return

            # Mã hóa mật khẩu mới
            new_password_hashed = hash_password(new_password)
            print(f"[DEBUG] New hashed password: {new_password_hashed}")

            # Cập nhật mật khẩu mới
            update_sinh_vien(
                student_data[0],  # ID_SV
                student_data[1],  # NAME_SV
                student_data[2],  # MSSV
                student_data[3],  # EMAIL_SV
                student_data[4],  # ADDRESS_SV
                student_data[5],  # DATE_SV
                student_data[6],  # SEX_SV
                student_data[7],  # CLASS_SV
                new_password_hashed,  # PASSWORD_SV
                student_data[8]   # PHONE_SV
            )

            # Hiển thị thông báo thành công
            self.show_dialog("Thành công", "Mật khẩu đã được thay đổi!")
            self.mssv_input.text = ""
            self.old_password.text = ""
            self.new_password.text = ""
            self.confirm_password.text = ""

        except Exception as e:
            self.show_dialog("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            print(f"[ERROR] Exception: {str(e)}")
        finally:
            conn.close()

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