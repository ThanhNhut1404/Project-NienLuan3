from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty
import numpy as np
import math
import sqlite3
from Database.Create_db import DB_NAME

# Màu sắc
PRIMARY_COLOR = "#2C387E"
BUTTON_COLOR = "#3F51B5"
TEXT_COLOR = "#000000"

# Font và kiểu
FONT_TITLE = "H5"
FONT_NORMAL = "Subtitle1"

# Kích thước
PADDING = 20
SPACING = 20


class PointChart(BoxLayout):
    chart_width = NumericProperty(200)  # Thu nhỏ biểu đồ
    chart_height = NumericProperty(200)  # Thu nhỏ biểu đồ

    def __init__(self, user=None, db_name=DB_NAME, title="Điểm rèn luyện học kỳ hiện tại", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = "300dp"  # Giảm chiều cao tổng thể
        self.padding = PADDING
        self.spacing = SPACING
        self.md_bg_color = [0.95, 0.95, 0.95, 1]  # Nền sáng nhẹ
        self.user = user
        self.db_name = db_name

        # Tiêu đề
        self.title_label = Label(
            text=f"[b][color={PRIMARY_COLOR.replace('#', '')}]{title}[/color][/b]",
            markup=True,
            font_size='20sp',  # Tương ứng với H5
            size_hint_y=None,
            height="40dp",
            halign='left',
            padding=[0, 0]
        )
        self.add_widget(self.title_label)

        # Thẻ chứa biểu đồ và nhãn
        self.card = MDCard(
            size_hint=(1, None),
            height="220dp",
            padding=PADDING,
            spacing=SPACING,
            md_bg_color=[0x3F / 255, 0x51 / 255, 0xB5 / 255, 0.2],  # BUTTON_COLOR với độ trong suốt
            radius=[10, 10, 10, 10]  # Bo góc
        )
        self.content_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=SPACING)

        # Widget cho biểu đồ
        self.chart_widget = Widget(size_hint_y=None, height=self.chart_height)
        self.content_layout.add_widget(self.chart_widget)

        # Nhãn chú thích tổng điểm
        self.score_label = Label(
            text="[color=000000]Tổng điểm học kỳ hiện tại: 0/100[/color]",
            markup=True,
            font_size='14sp',  # Tương ứng với Subtitle1
            size_hint_y=None,
            height="40dp",
            halign='left',
            valign='middle'
        )
        self.content_layout.add_widget(self.score_label)

        self.card.add_widget(self.content_layout)
        self.add_widget(self.card)

        self.texture = None
        self.rect = None
        self.setup_texture()
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.update_chart()

    def setup_texture(self):
        # Tạo texture với kích thước cố định và định dạng RGBA
        self.texture = Texture.create(size=(self.chart_width, self.chart_height), colorfmt='rgba', bufferfmt='ubyte')
        # Khởi tạo texture với màu nền trắng
        buf = np.ones((self.chart_height, self.chart_width, 4), dtype=np.uint8) * 255
        self.texture.blit_buffer(buf.ravel(), colorfmt='rgba', bufferfmt='ubyte')
        # Thêm texture vào canvas của chart_widget
        with self.chart_widget.canvas:
            Color(1, 1, 1, 1)  # Màu trắng cho nền
            self.rect = Rectangle(texture=self.texture, pos=self.chart_widget.pos,
                                  size=(self.chart_width, self.chart_height))

    def update_rect(self, *args):
        # Cập nhật vị trí và kích thước của rectangle
        self.rect.pos = self.chart_widget.pos
        self.rect.size = (self.chart_width, self.chart_height)

    def update_chart(self):
        # Lấy điểm học kỳ mới nhất từ database
        tong_diem = 0
        mssv = self.user.get("mssv") if self.user else None
        if mssv:
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    # Kiểm tra sự tồn tại của bảng HK_NK
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HK_NK'")
                    if not cursor.fetchone():
                        print("Lỗi: Bảng HK_NK không tồn tại trong cơ sở dữ liệu.")
                        self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Lỗi: Không tìm thấy bảng HK_NK[/color]"
                        return

                    # Kiểm tra sự tồn tại của bảng TONG_DIEM_HK
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TONG_DIEM_HK'")
                    if not cursor.fetchone():
                        print("Lỗi: Bảng TONG_DIEM_HK không tồn tại trong cơ sở dữ liệu.")
                        self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Lỗi: Không tìm thấy bảng TONG_DIEM_HK[/color]"
                        return

                    # Lấy ID học kỳ mới nhất
                    cursor.execute('''
                        SELECT ID_HK
                        FROM HK_NK
                        ORDER BY ID_HK DESC
                        LIMIT 1
                    ''')
                    result = cursor.fetchone()
                    if result:
                        id_hk = result[0]
                        # Lấy tổng điểm từ TONG_DIEM_HK
                        cursor.execute('''
                            SELECT TONG_DIEM
                            FROM TONG_DIEM_HK
                            WHERE ID_SV = ? AND ID_HK = ?
                        ''', (mssv, id_hk))
                        result = cursor.fetchone()
                        if result:
                            tong_diem = result[0]
                        else:
                            print(f"Không tìm thấy điểm cho MSSV {mssv} trong học kỳ {id_hk}.")
                            self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Không có điểm cho học kỳ mới nhất[/color]"
                    else:
                        print("Không tìm thấy học kỳ nào trong bảng HK_NK.")
                        self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Không có học kỳ nào trong cơ sở dữ liệu[/color]"
            except sqlite3.Error as e:
                print(f"Lỗi khi truy vấn cơ sở dữ liệu: {e}")
                self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Lỗi truy vấn: {e}[/color]"
        else:
            print("Lỗi: Không có MSSV được cung cấp.")
            self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Lỗi: Không có MSSV[/color]"

        diem_con_lai = max(0, 100 - tong_diem)
        if tong_diem > 0:
            self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Tổng điểm học kỳ mới nhất: {tong_diem}/100[/color]"

        # Tạo buffer cho biểu đồ
        buf = np.ones((self.chart_height, self.chart_width, 4), dtype=np.uint8) * 255  # Nền trắng

        # Tính toán thông số biểu đồ tròn
        center_x, center_y = self.chart_width // 2, self.chart_height // 2
        radius = min(self.chart_width, self.chart_height) // 2 - 20  # Bán kính, trừ lề
        angle = (tong_diem / 100) * 360  # Góc cho điểm hiện tại

        # Hàm chuyển đổi màu hex sang RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

        # Màu sắc
        color_achieved = hex_to_rgb("#4CAF50") + [255]  # Màu xanh lá
        color_remaining = hex_to_rgb("#B0BEC5") + [255]  # Màu xám

        # Vẽ biểu đồ tròn
        for y in range(self.chart_height):
            for x in range(self.chart_width):
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance <= radius:
                    point_angle = math.degrees(math.atan2(dy, dx)) % 360
                    if point_angle <= angle:
                        buf[y, x] = color_achieved  # Phần đã đạt
                    else:
                        buf[y, x] = color_remaining  # Phần còn lại

        # Làm phẳng buffer và đảm bảo kiểu uint8
        buf = buf.ravel()
        buf = buf.astype(np.uint8)

        # Kiểm tra kích thước buffer
        expected_size = self.chart_width * self.chart_height * 4
        if buf.size != expected_size:
            print(f"Lỗi: Kích thước buffer không khớp. Mong đợi: {expected_size}, Thực tế: {buf.size}")
            return

        # Cập nhật texture
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.chart_widget.canvas.ask_update()