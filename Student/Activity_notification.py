from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from datetime import datetime
import sqlite3
from Database.Create_db import DB_NAME

# Màu sắc
PRIMARY_COLOR = "#2C387E"
BUTTON_COLOR = "#3F51B5"
TEXT_COLOR = "#000000"
BUTTON_COLOR_RGBA = "#303F9F"

# Font và kiểu
FONT_TITLE = "H5"
FONT_NORMAL = "Subtitle1"

# Kích thước
PADDING = 20
SPACING = 20

class ActivityNotification(MDBoxLayout):
    notification_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = "200dp"
        self.padding = PADDING
        self.spacing = SPACING
        self.md_bg_color = [0.95, 0.95, 0.95, 1]  # Nền sáng nhẹ

        # Tiêu đề
        title_label = Label(
            text="[b][color=2C387E]Hoạt động sắp diễn ra[/color][/b]",
            markup=True,
            font_size='20sp',  # Tương ứng với H5
            size_hint_y=None,
            height="40dp",
            halign='left',  # Căn sát lề trái
            padding_x=0  # Không padding để sát lề trái
        )
        self.add_widget(title_label)

        # Thẻ thông báo
        self.card = MDCard(
            size_hint=(1, None),
            height="120dp",
            padding=PADDING,
            spacing=SPACING,
            md_bg_color=[0x3F/255, 0x51/255, 0xB5/255, 0.2],  # BUTTON_COLOR với độ trong suốt
            radius=[10, 10, 10, 10]  # Bo góc
        )
        self.content_layout = MDBoxLayout(orientation='vertical', padding=10)
        self.notification_label = Label(
            text="[color=000000]{}[/color]".format(self.notification_text),
            markup=True,
            font_size='14sp',  # Tương ứng với Subtitle1
            halign='left',
            valign='middle'
        )
        self.content_layout.add_widget(self.notification_label)
        self.card.add_widget(self.content_layout)
        self.add_widget(self.card)

        self.current_index = 0
        self.activities = []
        self.load_activities()
        if self.activities:
            self.update_notification()
            Clock.schedule_interval(self.switch_notification, 5)  # Chuyển thông báo mỗi 5 giây

    def load_activities(self):
        """Tải danh sách hoạt động chưa diễn ra từ cơ sở dữ liệu"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            current_date = datetime.now().strftime("%d/%m/%Y")
            cursor.execute('''
                SELECT TEN_HD, NGAY_TO_CHUC, DIA_CHI_HD, START_TIME 
                FROM HOAT_DONG 
                WHERE NGAY_TO_CHUC >= ?
                ORDER BY NGAY_TO_CHUC
            ''', (current_date,))
            self.activities = cursor.fetchall()
            conn.close()
        except Exception as e:
            print(f"Lỗi khi tải hoạt động: {e}")
            self.activities = []

    def update_notification(self):
        """Cập nhật nội dung thông báo"""
        if self.activities:
            activity = self.activities[self.current_index]
            ten_hd, ngay, dia_chi, gio = activity
            self.notification_text = (
                f"[b]Tên hoạt động:[/b] {ten_hd}\n"
                f"[b]Ngày tổ chức:[/b] {ngay}\n"
                f"[b]Địa điểm:[/b] {dia_chi}\n"
                f"[b]Giờ bắt đầu:[/b] {gio}"
            )
            self.notification_label.text = f"[color=000000]{self.notification_text}[/color]"
        else:
            self.notification_text = "Không có hoạt động sắp tới."
            self.notification_label.text = f"[color=000000]{self.notification_text}[/color]"

    def switch_notification(self, dt):
        """Chuyển đổi thông báo theo vòng lặp"""
        if self.activities:
            self.current_index = (self.current_index + 1) % len(self.activities)
            self.update_notification()