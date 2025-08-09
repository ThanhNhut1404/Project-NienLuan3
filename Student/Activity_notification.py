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
        self.last_activity_count = 0  # Lưu số lượng hoạt động để kiểm tra thay đổi
        self.load_activities()
        if self.activities:
            self.update_notification()
            Clock.schedule_interval(self.switch_notification, 5)  # Chuyển thông báo mỗi 5 giây
        Clock.schedule_interval(self.check_for_activity_updates, 30)  # Cập nhật mỗi 30 giây

    def load_activities(self):
        """Tải danh sách hoạt động chưa diễn ra trong học kỳ mới nhất từ cơ sở dữ liệu"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            current_date = datetime.now().strftime("%d/%m/%Y")

            # Kiểm tra bảng HK_NK tồn tại
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HK_NK'")
            if not cursor.fetchone():
                print("Lỗi: Bảng HK_NK không tồn tại.")
                self.activities = []
                self.notification_text = "Lỗi: Bảng HK_NK không tồn tại."
                self.notification_label.text = f"[color=000000]{self.notification_text}[/color]"
                conn.close()
                return

            # Lấy ID_HK và NAME_HK mới nhất từ HK_NK
            cursor.execute('''
                SELECT ID_HK, NAME_HK
                FROM HK_NK
                ORDER BY ID_HK DESC
                LIMIT 1
            ''')
            result = cursor.fetchone()
            if result:
                id_hk, name_hk = result
                # Lấy hoạt động thuộc học kỳ mới nhất
                cursor.execute('''
                    SELECT TEN_HD, NGAY_TO_CHUC, DIA_CHI_HD, START_TIME 
                    FROM HOAT_DONG 
                    WHERE ID_HK = ? AND NGAY_TO_CHUC >= ?
                    ORDER BY NGAY_TO_CHUC
                ''', (id_hk, current_date))
                self.activities = cursor.fetchall()
                if len(self.activities) != self.last_activity_count:
                    print(f"Debug: Học kỳ mới nhất - ID_HK: {id_hk}, NAME_HK: {name_hk}, Tìm thấy {len(self.activities)} hoạt động")
                    self.last_activity_count = len(self.activities)
                if self.activities:
                    self.update_notification()
                else:
                    self.notification_text = f"Không có hoạt động sắp tới trong học kỳ {name_hk}."
                    self.notification_label.text = f"[color=000000]{self.notification_text}[/color]"
            else:
                print("Debug: Không tìm thấy học kỳ nào trong bảng HK_NK.")
                self.activities = []
                self.notification_text = "Không có học kỳ nào trong cơ sở dữ liệu."
                self.notification_label.text = f"[color=000000]{self.notification_text}[/color]"
            conn.close()
        except sqlite3.Error as e:
            print(f"Lỗi khi tải hoạt động: {e}")
            self.activities = []
            self.notification_text = f"Lỗi khi tải hoạt động: {e}"
            self.notification_label.text = f"[color=000000]{self.notification_text}[/color]"

    def check_for_activity_updates(self, dt):
        """Kiểm tra cập nhật danh sách hoạt động."""
        self.load_activities()

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
            self.notification_text = "Không có hoạt động sắp tới trong học kỳ này."
            self.notification_label.text = f"[color=000000]{self.notification_text}[/color]"

    def switch_notification(self, dt):
        """Chuyển đổi thông báo theo vòng lặp"""
        if self.activities:
            self.current_index = (self.current_index + 1) % len(self.activities)
            self.update_notification()