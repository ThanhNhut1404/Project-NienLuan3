from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp
from kivy.metrics import dp
import shutil
import os
from datetime import datetime
import sqlite3
from Database.Create_db import DB_NAME
from PIL import Image as PILImage

# Màu sắc và kích thước từ cấu hình
PRIMARY_COLOR = "#2C387E"
BUTTON_COLOR = "#3F51B5"
TEXT_COLOR = "#000000"
BUTTON_COLOR_RGBA = "#303F9F"
FONT_TITLE = "H5"
FONT_NORMAL = "Subtitle2"
WINDOW_WIDTH = 360
WINDOW_HEIGHT = 640
BUTTON_HEIGHT = 56
PADDING = 20
SPACING = 12


class UpdateStudentScreen(MDScreen):
    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        self.user = user or {}
        self.image_path = ""
        self.dialog = None
        self.date_dialog = None
        self.load_user_data()
        self.build_ui()

    def load_user_data(self):
        if self.user.get("mssv"):
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT NAME_SV, MSSV, EMAIL_SV, ADDRESS_SV, DATE_SV, SEX_SV, PHONE_SV, IMG
                    FROM SINH_VIEN 
                    WHERE MSSV = ?
                """, (self.user.get("mssv"),))
                result = cursor.fetchone()
                conn.close()

                if result:
                    self.user["name"] = result[0] or ""
                    self.user["mssv"] = result[1] or ""
                    self.user["email"] = result[2] or ""
                    self.user["address"] = result[3] or ""
                    self.user["dob"] = result[4] or "01-01-2000"
                    self.user["sex"] = result[5] if result[5] is not None else 1
                    self.user["phone"] = result[6] or ""
                    self.user["avatar"] = result[7] or "default_avatar.png"
                else:
                    self.user.setdefault("name", "")
                    self.user.setdefault("mssv", "")
                    self.user.setdefault("email", "")
                    self.user.setdefault("address", "")
                    self.user.setdefault("dob", "01-01-2000")
                    self.user.setdefault("sex", 1)
                    self.user.setdefault("phone", "")
                    self.user.setdefault("avatar", "default_avatar.png")
            except Exception as e:
                print(f"Debug - Error loading user data: {e}")
                self.user.setdefault("name", "")
                self.user.setdefault("mssv", "")
                self.user.setdefault("email", "")
                self.user.setdefault("address", "")
                self.user.setdefault("dob", "01-01-2000")
                self.user.setdefault("sex", 1)
                self.user.setdefault("phone", "")
                self.user.setdefault("avatar", "default_avatar.png")
        else:
            print("Debug - No MSSV provided")
            self.user.setdefault("name", "")
            self.user.setdefault("mssv", "")
            self.user.setdefault("email", "")
            self.user.setdefault("address", "")
            self.user.setdefault("dob", "01-01-2000")
            self.user.setdefault("sex", 1)
            self.user.setdefault("phone", "")
            self.user.setdefault("avatar", "default_avatar.png")

    def load_user(self, user):
        self.user = user or {}
        self.load_user_data()
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(5),
            padding=dp(5),
            md_bg_color=[1, 1, 1, 1]
        )

        toolbar = MDTopAppBar(
            title="Cập nhật thông tin sinh viên",
            left_action_items=[["arrow-left", lambda x: self.go_back(x)]],
            md_bg_color=PRIMARY_COLOR,
            size_hint_y=None,
            height=dp(BUTTON_HEIGHT)
        )
        main_layout.add_widget(toolbar)

        scroll = MDScrollView()
        outer = MDBoxLayout(
            orientation='vertical',
            padding=dp(PADDING),
            spacing=dp(SPACING),
            size_hint_y=None
        )
        outer.bind(minimum_height=outer.setter('height'))
        scroll.add_widget(outer)

        info_card = MDCard(
            orientation='vertical',
            padding=dp(8),
            spacing=dp(12),
            size_hint=(1, None),
            pos_hint={"center_x": 0.5}
        )
        info_card.bind(minimum_height=info_card.setter('height'))
        outer.add_widget(info_card)

        title = MDLabel(
            text="🔄 Cập nhật thông tin",
            font_style=FONT_TITLE,
            theme_text_color="Custom",
            text_color=TEXT_COLOR,
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        info_card.add_widget(title)

        # AVATAR
        avatar_filename = self.user.get("avatar", "default_avatar.png")
        image_path = os.path.join("assets", avatar_filename)
        if not os.path.exists(image_path):
            print(f"Debug - Không tìm thấy {image_path}, tạo ảnh mặc định")
            if not os.path.exists("assets"):
                os.makedirs("assets")
            image_path = os.path.join("assets", "default_avatar.png")
            PILImage.new("RGB", (80, 80), color=(200, 200, 200)).save(image_path)

        avatar_card = MDCard(
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            radius=[dp(40)],
            md_bg_color=[1, 1, 1, 1],
            pos_hint={"center_x": 0.5}
        )
        self.avatar = Image(
            source=image_path,
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        avatar_card.add_widget(self.avatar)
        info_card.add_widget(avatar_card)

        choose_image_label = MDLabel(
            text="Chọn ảnh",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=BUTTON_COLOR_RGBA,
            halign="center",
            size_hint_y=None,
            height=dp(20),
            on_touch_down=self.on_choose_image_label_touch
        )
        info_card.add_widget(choose_image_label)

        def add_field(label, value, hint):
            row = MDBoxLayout(
                orientation='horizontal',
                padding=dp(5),
                spacing=dp(5),
                size_hint_y=None,
                height=dp(35)
            )
            row.add_widget(
                MDLabel(
                    text=label,
                    font_style=FONT_NORMAL,
                    halign="left",
                    size_hint_x=None,
                    width=dp(70),
                    theme_text_color="Custom",
                    text_color=TEXT_COLOR
                )
            )
            text_field = MDTextField(
                text=value,
                hint_text=hint,
                mode="rectangle",
                line_color_focus=PRIMARY_COLOR,
                hint_text_color_normal=[0.7, 0.7, 0.7, 1],
                size_hint_x=1,
                font_size=dp(12)
            )
            row.add_widget(text_field)
            info_card.add_widget(row)
            return text_field

        # Trường tên (đầu tiên)
        self.name_field = add_field("🧑 Họ tên:", self.user.get("name", ""), "Nhập họ tên")
        self.email_field = add_field("📧 Email:", self.user.get("email", ""), "Nhập email")
        self.address_field = add_field("🏠 Địa chỉ:", self.user.get("address", ""), "Nhập địa chỉ")

        # Trường ngày sinh
        dob_row = MDBoxLayout(
            orientation='horizontal',
            padding=dp(5),
            spacing=dp(5),
            size_hint_y=None,
            height=dp(35)
        )
        dob_row.add_widget(
            MDLabel(
                text="🎂 Ngày sinh:",
                font_style=FONT_NORMAL,
                halign="left",
                size_hint_x=None,
                width=dp(70),
                theme_text_color="Custom",
                text_color=TEXT_COLOR
            )
        )
        dob_sub_row = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint_x=1
        )
        self.dob_field = MDTextField(
            text=self.user.get("dob", "01-01-2000"),
            hint_text="Ngày sinh (dd-mm-yyyy)",
            mode="rectangle",
            line_color_focus=PRIMARY_COLOR,
            hint_text_color_normal=[0.7, 0.7, 0.7, 1],
            size_hint_x=0.7,
            font_size=dp(12)
        )
        select_date_btn = MDRectangleFlatButton(
            icon="calendar",
            md_bg_color=BUTTON_COLOR,
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            on_release=self.show_date_picker
        )
        dob_sub_row.add_widget(self.dob_field)
        dob_sub_row.add_widget(select_date_btn)
        dob_row.add_widget(dob_sub_row)
        info_card.add_widget(dob_row)

        self.phone_field = add_field("📞 SĐT:", self.user.get("phone", ""), "Nhập số điện thoại")

        # Trường giới tính (cuối cùng)
        sex_row = MDBoxLayout(
            orientation='horizontal',
            padding=dp(5),
            spacing=dp(5),
            size_hint_y=None,
            height=dp(35)
        )
        sex_row.add_widget(
            MDLabel(
                text="👤 Giới tính:",
                font_style=FONT_NORMAL,
                halign="left",
                size_hint_x=None,
                width=dp(70),
                theme_text_color="Custom",
                text_color=TEXT_COLOR
            )
        )
        self.sex_field = Spinner(
            text="Nam" if self.user.get("sex", 1) == 1 else "Nữ",
            values=["Nam", "Nữ"],
            size_hint=(1, None),
            height=dp(35),
            background_color=PRIMARY_COLOR,
            color=(1, 1, 1, 1)
        )
        sex_row.add_widget(self.sex_field)
        info_card.add_widget(sex_row)

        update_btn = MDRectangleFlatButton(
            text="Lưu",
            md_bg_color=BUTTON_COLOR,
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(100), dp(35)),
            on_release=self.update_info
        )
        outer.add_widget(update_btn)

        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def on_choose_image_label_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.choose_image(instance)

    def show_date_picker(self, instance):
        if self.date_dialog:
            self.date_dialog.dismiss()

        d, m, y = "01", "01", "2000"
        dob_str = self.user.get("dob", "01-01-2000")
        if dob_str:
            try:
                d, m, y = dob_str.split("-")
            except:
                pass

        day_spinner = Spinner(
            text=d,
            values=[str(i).zfill(2) for i in range(1, 32)],
            size_hint_y=None,
            height=dp(35),
            background_color=PRIMARY_COLOR,
            color=(1, 1, 1, 1)
        )
        month_spinner = Spinner(
            text=m,
            values=[str(i).zfill(2) for i in range(1, 13)],
            size_hint_y=None,
            height=dp(35),
            background_color=PRIMARY_COLOR,
            color=(1, 1, 1, 1)
        )
        year_spinner = Spinner(
            text=y,
            values=[str(i) for i in range(1970, 2031)],
            size_hint_y=None,
            height=dp(35),
            background_color=PRIMARY_COLOR,
            color=(1, 1, 1, 1)
        )

        def on_confirm(*args):
            new_dob = f"{day_spinner.text}-{month_spinner.text}-{year_spinner.text}"
            self.dob_field.text = new_dob
            self.date_dialog.dismiss()

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(8),
            md_bg_color=[1, 1, 1, 1]
        )
        content.add_widget(
            MDLabel(
                text="Chọn ngày sinh:",
                font_style=FONT_NORMAL,
                halign="center",
                theme_text_color="Custom",
                text_color=TEXT_COLOR
            )
        )
        spinner_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            pos_hint={"center_x": 0.5}
        )
        spinner_layout.add_widget(day_spinner)
        spinner_layout.add_widget(month_spinner)
        spinner_layout.add_widget(year_spinner)
        content.add_widget(spinner_layout)
        content.add_widget(
            MDRectangleFlatButton(
                text="Xác nhận",
                md_bg_color=BUTTON_COLOR,
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
                pos_hint={"center_x": 0.5},
                size_hint=(None, None),
                size=(dp(100), dp(35)),
                on_release=on_confirm
            )
        )

        self.date_dialog = Popup(
            title="Chọn ngày sinh",
            content=content,
            size_hint=(0.8, 0.5),
            background_color=[0.9, 0.9, 0.9, 1]
        )
        self.date_dialog.open()

    def choose_image(self, instance):
        chooser_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(8),
            md_bg_color=[1, 1, 1, 1]
        )
        file_chooser = FileChooserListView(filters=["*.png", "*.jpg", "*.jpeg"])
        chooser_layout.add_widget(file_chooser)

        def on_select(_):
            selection = file_chooser.selection
            if selection:
                self.image_path = selection[0]
                self.avatar.source = self.image_path
                self.avatar.reload()
                self.popup.dismiss()

        choose_btn = MDRectangleFlatButton(
            text="Chọn",
            md_bg_color=BUTTON_COLOR,
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(100), dp(35)),
            on_release=on_select
        )
        chooser_layout.add_widget(choose_btn)

        self.popup = Popup(
            title="Chọn ảnh",
            content=chooser_layout,
            size_hint=(0.9, 0.9),
            background_color=[0.9, 0.9, 0.9, 1]
        )
        self.popup.open()

    def show_popup(self, title, text):
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=title,
            text=text,
            md_bg_color=[1, 1, 1, 1],
            buttons=[
                MDRectangleFlatButton(
                    text="OK",
                    md_bg_color=BUTTON_COLOR,
                    theme_text_color="Custom",
                    text_color=[1, 1, 1, 1],
                    size_hint=(None, None),
                    size=(dp(100), dp(35)),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def update_info(self, instance):
        name = self.name_field.text.strip()
        email = self.email_field.text.strip()
        address = self.address_field.text.strip()
        dob = self.dob_field.text.strip() or self.user.get("dob", "01-01-2000")
        sex = 1 if self.sex_field.text == "Nam" else 0
        phone = self.phone_field.text.strip()
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
                return

        try:
            try:
                datetime.strptime(dob, "%d-%m-%Y")
            except ValueError:
                self.show_popup("❌ Lỗi", "Định dạng ngày sinh phải là dd-mm-yyyy.")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            mssv = self.user.get("mssv")
            id_sv = self.user.get("id")
            if not mssv or not id_sv:
                self.show_popup("❌ Lỗi", "Thiếu MSSV hoặc ID, không thể cập nhật.")
                conn.close()
                return

            # Kiểm tra email trùng
            cursor.execute("SELECT ID_SV FROM SINH_VIEN WHERE EMAIL_SV = ? AND ID_SV != ?", (email, id_sv))
            if cursor.fetchone():
                self.show_popup("❌ Lỗi", "Email đã được sử dụng.")
                conn.close()
                return

            cursor.execute("""
                UPDATE SINH_VIEN 
                SET NAME_SV = ?, EMAIL_SV = ?, ADDRESS_SV = ?, DATE_SV = ?, SEX_SV = ?, PHONE_SV = ?, IMG = ?
                WHERE ID_SV = ?
            """, (name or self.user.get("name", ""), email or self.user.get("email", ""),
                  address or self.user.get("address", ""), dob, sex,
                  phone or self.user.get("phone", ""), avatar_filename, id_sv))
            conn.commit()
            conn.close()

            # Cập nhật dữ liệu trong user
            self.user["name"] = name or self.user.get("name", "")
            self.user["email"] = email or self.user.get("email", "")
            self.user["address"] = address or self.user.get("address", "")
            self.user["dob"] = dob
            self.user["sex"] = sex
            self.user["phone"] = phone or self.user.get("phone", "")
            self.user["avatar"] = avatar_filename

            # Làm mới dữ liệu trên ViewInforScreen
            try:
                view_infor_screen = self.manager.get_screen("view_infor")
                view_infor_screen.load_user(self.user)
            except Exception as e:
                print(f"Debug - Lỗi khi làm mới ViewInforScreen: {e}")

            self.show_popup("✅ Thành công", "Cập nhật thông tin thành công!")
            self.manager.current = "view_infor"  # Chuyển về ViewInforScreen

        except Exception as e:
            self.show_popup("❌ Lỗi", f"Lỗi khi cập nhật: {e}")
            print(f"Debug - Lỗi: {e}")

    def go_back(self, instance):
        self.manager.current = "view_infor"  # Chuyển về ViewInforScreen