from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
import shutil
import os
import hashlib
from datetime import datetime
import sqlite3
from Database.Create_db import DB_NAME
from PIL import Image as PILImage

class UpdateStudentScreen(MDScreen):
    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        self.user = user or {}
        self.user.setdefault("address", "")
        self.user.setdefault("phone", "")
        self.user.setdefault("dob", "01-01-2000")
        self.user.setdefault("avatar", "default_avatar.png")
        self.user.setdefault("password", "")
        self.user.setdefault("mssv", "")
        self.image_path = ""
        self.dialog = None
        self.date_dialog = None
        self.build_ui()

    def load_user(self, user):
        self.user = user or {}
        self.user.setdefault("address", "")
        self.user.setdefault("phone", "")
        self.user.setdefault("dob", "01-01-2000")
        self.user.setdefault("avatar", "default_avatar.png")
        self.user.setdefault("password", "")
        self.user.setdefault("mssv", "")
        if not self.user.get("mssv"):
            print("Debug - Thiếu MSSV trong user data")
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        scroll_view = MDScrollView()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        layout.add_widget(MDLabel(text="🔄 Cập nhật thông tin sinh viên", halign="center", font_style="H6"))

        avatar_source = os.path.join("assets", self.user.get("avatar"))
        if not os.path.exists(avatar_source):
            print(f"Debug - Không tìm thấy {avatar_source}, dùng default_avatar.png")
            avatar_source = "default_avatar.png"
            if not os.path.exists(avatar_source):
                print("Debug - Tạo file default_avatar.png placeholder")
                if not os.path.exists("assets"):
                    os.makedirs("assets")
                PILImage.new("RGB", (100, 100), color=(255, 255, 255)).save(os.path.join("assets", "default_avatar.png"))
        self.avatar = Image(source=avatar_source, size_hint=(1, 0.4), allow_stretch=True, keep_ratio=True)
        layout.add_widget(self.avatar)

        layout.add_widget(MDRaisedButton(text="📁 Chọn ảnh", on_release=self.choose_image))

        self.address_field = MDTextField(hint_text="Địa chỉ", text=self.user.get("address", ""), mode="rectangle")
        self.phone_field = MDTextField(hint_text="Số điện thoại", text=self.user.get("phone", ""), mode="rectangle")

        # Chỉ hiển thị trường nhập ngày sinh và nút chọn ngày
        dob_str = self.user.get("dob", "01-01-2000")
        self.dob_field = MDTextField(hint_text="Ngày sinh (dd-mm-yyyy)", text=dob_str, mode="rectangle", size_hint_x=0.8)
        select_date_btn = MDRaisedButton(text="📅 Chọn ngày", size_hint_x=0.2, on_release=self.show_date_picker)
        dob_layout = MDBoxLayout(orientation="horizontal", spacing=10, size_hint_y=None)
        dob_layout.add_widget(self.dob_field)
        dob_layout.add_widget(select_date_btn)

        layout.add_widget(self.address_field)
        layout.add_widget(self.phone_field)
        layout.add_widget(dob_layout)

        self.old_pw_field = MDTextField(hint_text="Mật khẩu cũ", password=True, mode="rectangle")
        self.new_pw_field = MDTextField(hint_text="Mật khẩu mới", password=True, mode="rectangle")
        self.confirm_new_pw_field = MDTextField(hint_text="Xác nhận mật khẩu mới", password=True, mode="rectangle")

        layout.add_widget(self.old_pw_field)
        layout.add_widget(self.new_pw_field)
        layout.add_widget(self.confirm_new_pw_field)

        layout.add_widget(MDRaisedButton(text="💾 Cập nhật", on_release=self.update_info))
        layout.add_widget(MDRaisedButton(text="← Quay lại", on_release=self.go_back))

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def show_date_picker(self, instance):
        if self.date_dialog:
            self.date_dialog.dismiss()

        d, m, y = "01", "01", "2000"
        dob_str = self.dob_field.text.strip()
        if dob_str:
            try:
                d, m, y = dob_str.split("-")
            except:
                pass

        day_spinner = Spinner(text=d, values=[str(i).zfill(2) for i in range(1, 32)], size_hint_y=None, height="40dp")
        month_spinner = Spinner(text=m, values=[str(i).zfill(2) for i in range(1, 13)], size_hint_y=None, height="40dp")
        year_spinner = Spinner(text=y, values=[str(i) for i in range(1970, 2031)], size_hint_y=None, height="40dp")

        def on_confirm(*args):
            new_dob = f"{day_spinner.text}-{month_spinner.text}-{year_spinner.text}"
            self.dob_field.text = new_dob
            self.date_dialog.dismiss()

        content = MDBoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(MDLabel(text="Chọn ngày sinh:", halign="center"))
        spinner_layout = MDBoxLayout(orientation="horizontal", spacing=10)
        spinner_layout.add_widget(day_spinner)
        spinner_layout.add_widget(month_spinner)
        spinner_layout.add_widget(year_spinner)
        content.add_widget(spinner_layout)
        content.add_widget(MDRaisedButton(text="Xác nhận", on_release=on_confirm))

        self.date_dialog = Popup(title="Chọn ngày sinh", content=content, size_hint=(0.8, 0.5))
        self.date_dialog.open()

    def choose_image(self, instance):
        chooser_layout = MDBoxLayout(orientation="vertical", spacing=10)
        file_chooser = FileChooserListView(filters=["*.png", "*.jpg", "*.jpeg"])
        chooser_layout.add_widget(file_chooser)

        def on_select(_):
            selection = file_chooser.selection
            if selection:
                self.image_path = selection[0]
                self.avatar.source = self.image_path
                self.popup.dismiss()

        choose_btn = MDRaisedButton(text="Chọn", on_release=on_select)
        chooser_layout.add_widget(choose_btn)

        self.popup = Popup(title="Chọn ảnh", content=chooser_layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def show_popup(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(title=title, text=text)
        self.dialog.open()

    def update_info(self, instance):
        address = self.address_field.text.strip()
        phone = self.phone_field.text.strip()

        dob_input = self.dob_field.text.strip()
        if not dob_input:
            dob_input = "01-01-2000"  # Mặc định nếu trống
        dob = dob_input or self.user.get("dob", "01-01-2000")

        old_pw = self.old_pw_field.text.strip()
        new_pw = self.new_pw_field.text.strip()
        confirm_new_pw = self.confirm_new_pw_field.text.strip()
        avatar_filename = self.user.get("avatar", "default_avatar.png")

        if self.image_path:
            avatar_filename = os.path.basename(self.image_path)
            dest_path = os.path.join("assets", avatar_filename)
            try:
                if not os.path.exists("assets"):
                    os.makedirs("assets")
                shutil.copy(self.image_path, dest_path)
            except Exception as e:
                self.show_popup("❌ Lỗi", f"Không thể sao chép ảnh: {e}")

        try:
            current_pw_hashed = self.user.get("password", "")
            if old_pw:
                if hashlib.sha256(old_pw.encode()).hexdigest() != current_pw_hashed:
                    self.show_popup("❌ Lỗi", "Mật khẩu cũ không đúng.")
                    return
                if new_pw != confirm_new_pw:
                    self.show_popup("❌ Lỗi", "Mật khẩu mới và xác nhận mật khẩu không khớp.")
                    return
                if len(new_pw) < 9 or not any(c.isupper() for c in new_pw) or not any(c.isdigit() for c in new_pw):
                    self.show_popup("⚠️ Mật khẩu yếu", "Mật khẩu mới phải có ít nhất 9 ký tự, gồm chữ hoa và số.")
                    return
                final_password = hashlib.sha256(new_pw.encode()).hexdigest()
            else:
                final_password = current_pw_hashed

            dob_db = dob
            try:
                datetime.strptime(dob_db, "%d-%m-%Y")
            except ValueError:
                self.show_popup("❌ Lỗi", "Định dạng ngày sinh phải là dd-mm-yyyy.")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            mssv = self.user.get("mssv")
            if not mssv:
                self.show_popup("❌ Lỗi", "Thiếu MSSV, không thể cập nhật.")
                conn.close()
                return
            cursor.execute("""
                UPDATE SINH_VIEN 
                SET ADDRESS_SV = ?, PHONE_SV = ?, DATE_SV = ?, PASSWORD_SV = ?, IMG = ? 
                WHERE MSSV = ?
            """, (address or self.user.get("address", ""), phone or self.user.get("phone", ""), dob_db, final_password, avatar_filename, mssv))
            conn.commit()
            conn.close()

            self.user["address"] = address or self.user.get("address", "")
            self.user["phone"] = phone or self.user.get("phone", "")
            self.user["dob"] = dob or self.user.get("dob", "")
            self.user["avatar"] = avatar_filename
            self.user["password"] = final_password

            self.show_popup("✅ Thành công", "Cập nhật thông tin thành công!")

        except Exception as e:
            self.show_popup("❌ Lỗi", f"Lỗi khi cập nhật: {e}")
            print(f"Debug - Lỗi: {e}")

    def go_back(self, instance):
        self.manager.current = "student_main"