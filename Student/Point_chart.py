from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty
from kivy.clock import Clock
import numpy as np
import math
import sqlite3
from Database.Create_db import DB_NAME

# Màu sắc
PRIMARY_COLOR = "#2C387E"
BUTTON_COLOR = "#3F51B5"
TEXT_COLOR = "#000000"
ACHIEVED_COLOR = "#4CAF50"
REMAINING_COLOR = "#B0BEC5"
BORDER_COLOR = "#E0E0E0"

# Font và kiểu
FONT_TITLE = "H5"
FONT_NORMAL = "Subtitle1"

# Kích thước
PADDING = 20
SPACING = 15

class PointChart(BoxLayout):
    chart_width = NumericProperty(200)
    chart_height = NumericProperty(200)

    def __init__(self, user=None, db_name=DB_NAME, title="Điểm rèn luyện học kỳ hiện tại", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)  # Full chiều ngang
        self.height = "340dp"
        self.padding = [0, PADDING, 0, PADDING]  # Bỏ padding trái-phải
        self.spacing = SPACING
        self.md_bg_color = [0.98, 0.98, 0.98, 1]
        self.user = user
        self.db_name = db_name
        self.last_diem_danh_count = 0
        self.last_tong_diem = None  # Lưu điểm tổng cuối cùng để so sánh

        # Tiêu đề
        self.title_label = Label(
            text=f"[b][color={PRIMARY_COLOR.replace('#', '')}]{title}[/color][/b]",
            markup=True,
            font_size='22sp',
            size_hint_y=None,
            height="40dp",
            halign='center',
            padding=[0, 10, 0, 10]
        )
        self.add_widget(self.title_label)

        # Thẻ chứa biểu đồ
        self.card = MDCard(
            size_hint=(1, None),
            height="260dp",
            padding=PADDING,
            spacing=SPACING,
            md_bg_color=[1, 1, 1, 1]
        )
        self.content_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=SPACING)

        # Container căn giữa biểu đồ
        self.chart_container = BoxLayout(
            size_hint=(1, None),  # Full chiều ngang
            height="160dp",
            padding=[0, 10, 0, 10]
        )
        self.chart_widget = Widget(size_hint=(None, None), size=(self.chart_width, self.chart_height))
        self.chart_container.add_widget(self.chart_widget)
        self.content_layout.add_widget(self.chart_container)

        # Chú thích màu sắc
        self.legend_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="30dp",
            spacing=10,
            padding=[10, 0, 10, 0]
        )
        self.legend_achieved = MDBoxLayout(orientation='horizontal', spacing=5)
        self.legend_achieved_color = Widget(size_hint_x=None, width=20)
        with self.legend_achieved_color.canvas.before:
            Color(rgba=[76/255, 175/255, 80/255, 1])
            self.legend_achieved_rect = Rectangle(pos=self.legend_achieved_color.pos, size=(20, 20))
        self.legend_achieved_color.bind(pos=self.update_legend_achieved)
        self.legend_achieved.add_widget(self.legend_achieved_color)
        self.legend_achieved.add_widget(Label(
            text="[color=000000]Điểm đạt được[/color]",
            markup=True,
            font_size='12sp',
            size_hint_y=None,
            height="20dp"
        ))
        self.legend_remaining = MDBoxLayout(orientation='horizontal', spacing=5)
        self.legend_remaining_color = Widget(size_hint_x=None, width=20)
        with self.legend_remaining_color.canvas.before:
            Color(rgba=[176/255, 190/255, 197/255, 1])
            self.legend_remaining_rect = Rectangle(pos=self.legend_remaining_color.pos, size=(20, 20))
        self.legend_remaining_color.bind(pos=self.update_legend_remaining)
        self.legend_remaining.add_widget(self.legend_remaining_color)
        self.legend_remaining.add_widget(Label(
            text="[color=000000]Điểm cần đạt[/color]",
            markup=True,
            font_size='12sp',
            size_hint_y=None,
            height="20dp"
        ))
        self.legend_layout.add_widget(self.legend_achieved)
        self.legend_layout.add_widget(self.legend_remaining)
        self.content_layout.add_widget(self.legend_layout)

        # Nhãn tổng điểm
        self.score_label = Label(
            text="[color=000000]Tổng điểm học kỳ hiện tại: 0/100[/color]",
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            height="30dp",
            halign='center',
            valign='middle',
            padding=[0, 5, 0, 5]
        )
        self.content_layout.add_widget(self.score_label)

        self.card.add_widget(self.content_layout)
        self.add_widget(self.card)

        self.texture = None
        self.rect = None
        self.setup_texture()
        self.bind(pos=self.update_rect, size=self.update_rect)
        Clock.schedule_once(lambda dt: self.update_chart(), 0)
        # Kiểm tra cập nhật mỗi 2 giây
        Clock.schedule_interval(self.check_for_updates, 2)

    def setup_texture(self):
        self.texture = Texture.create(size=(self.chart_width, self.chart_height), colorfmt='rgba', bufferfmt='ubyte')
        buf = np.ones((self.chart_height, self.chart_width, 4), dtype=np.uint8) * 255
        self.texture.blit_buffer(buf.ravel(), colorfmt='rgba', bufferfmt='ubyte')
        with self.chart_widget.canvas.before:
            Color(rgba=[224/255, 224/255, 224/255, 1])
            self.border_ellipse = Ellipse(size=(self.chart_width, self.chart_height))
            Color(1, 1, 1, 1)
            self.rect = Rectangle(texture=self.texture, size=(self.chart_width, self.chart_height))
        self.chart_widget.bind(pos=self.update_rect, size=self.update_rect)  # Bind cả pos và size

    def update_rect(self, *args):
        # Tính toán vị trí để căn giữa biểu đồ trong chart_container
        chart_x = self.chart_container.x + (self.chart_container.width - self.chart_width) / 2
        chart_y = self.chart_container.y + (self.chart_container.height - self.chart_height) / 2
        self.chart_widget.pos = (chart_x, chart_y)
        self.rect.pos = (chart_x, chart_y)
        self.border_ellipse.pos = (chart_x, chart_y)
        self.rect.size = (self.chart_width, self.chart_height)
        self.border_ellipse.size = (self.chart_width, self.chart_height)

    def update_legend_achieved(self, instance, value):
        self.legend_achieved_rect.pos = instance.pos

    def update_legend_remaining(self, instance, value):
        self.legend_remaining_rect.pos = instance.pos

    def check_for_updates(self, dt):
        """Kiểm tra thay đổi trong TONG_DIEM_HK."""
        if not self.user:
            return
        mssv = self.user.get("mssv")
        if not mssv:
            return

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT ID_HK
                    FROM HK_NK
                    ORDER BY ID_HK DESC
                    LIMIT 1
                ''')
                result = cursor.fetchone()
                if result:
                    id_hk = result[0]
                    cursor.execute('''
                        SELECT TONG_DIEM
                        FROM TONG_DIEM_HK
                        WHERE ID_SV = ? AND ID_HK = ?
                    ''', (mssv, id_hk))
                    result = cursor.fetchone()
                    current_tong_diem = result[0] if result else 0
                    if current_tong_diem != self.last_tong_diem:
                        print(f"Debug: Điểm tổng thay đổi từ {self.last_tong_diem} thành {current_tong_diem}")
                        self.last_tong_diem = current_tong_diem
                        self.update_chart()
        except sqlite3.Error as e:
            print(f"Lỗi khi kiểm tra cập nhật: {e}")

    def update_chart(self):
        """Cập nhật biểu đồ và nhãn điểm từ DB."""
        tong_diem = 0
        mssv = self.user.get("mssv") if self.user else None
        if not mssv:
            print("Debug - Không có MSSV được cung cấp")
            self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Chưa đăng nhập hoặc không có MSSV[/color]"
            self.draw_empty_chart()
            return

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HK_NK'")
                if not cursor.fetchone():
                    print("Lỗi: Bảng HK_NK không tồn tại trong cơ sở dữ liệu.")
                    self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Lỗi: Không tìm thấy bảng HK_NK[/color]"
                    self.draw_empty_chart()
                    return

                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TONG_DIEM_HK'")
                if not cursor.fetchone():
                    print("Lỗi: Bảng TONG_DIEM_HK không tồn tại trong cơ sở dữ liệu.")
                    self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Lỗi: Không tìm thấy bảng TONG_DIEM_HK[/color]"
                    self.draw_empty_chart()
                    return

                cursor.execute('''
                    SELECT ID_HK
                    FROM HK_NK
                    ORDER BY ID_HK DESC
                    LIMIT 1
                ''')
                result = cursor.fetchone()
                if result:
                    id_hk = result[0]
                    cursor.execute('''
                        SELECT TONG_DIEM
                        FROM TONG_DIEM_HK
                        WHERE ID_SV = ? AND ID_HK = ?
                    ''', (mssv, id_hk))
                    result = cursor.fetchone()
                    if result:
                        tong_diem = result[0]
                        self.last_tong_diem = tong_diem  # Cập nhật điểm tổng cuối cùng
                    else:
                        print(f"Không tìm thấy điểm cho MSSV {mssv} trong học kỳ {id_hk}.")
                        self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Không có điểm cho học kỳ mới nhất[/color]"
                        self.draw_empty_chart()
                        return
                else:
                    print("Không tìm thấy học kỳ nào trong bảng HK_NK.")
                    self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Không có học kỳ nào trong cơ sở dữ liệu[/color]"
                    self.draw_empty_chart()
                    return
        except sqlite3.Error as e:
            print(f"Lỗi khi truy vấn cơ sở dữ liệu: {e}")
            self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Lỗi truy vấn: {e}[/color]"
            self.draw_empty_chart()
            return

        diem_con_lai = max(0, 100 - tong_diem)
        self.score_label.text = f"[color={TEXT_COLOR.replace('#', '')}]Tổng điểm học kỳ hiện tại: {tong_diem}/100[/color]"

        buf = np.ones((self.chart_height, self.chart_width, 4), dtype=np.uint8) * 255
        center_x, center_y = self.chart_width // 2, self.chart_height // 2
        radius = min(self.chart_width, self.chart_height) // 2 - 22
        angle = (tong_diem / 100) * 360

        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

        color_achieved = hex_to_rgb(ACHIEVED_COLOR) + [255]
        color_remaining = hex_to_rgb(REMAINING_COLOR) + [255]

        for y in range(self.chart_height):
            for x in range(self.chart_width):
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance <= radius:
                    point_angle = math.degrees(math.atan2(dy, dx)) % 360
                    if point_angle <= angle:
                        buf[y, x] = color_achieved
                    else:
                        buf[y, x] = color_remaining

        buf = buf.ravel()
        buf = buf.astype(np.uint8)
        expected_size = self.chart_width * self.chart_height * 4
        if buf.size != expected_size:
            print(f"Lỗi: Kích thước buffer không khớp. Mong đợi: {expected_size}, Thực tế: {buf.size}")
            return

        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.chart_widget.canvas.ask_update()

    def draw_empty_chart(self):
        buf = np.ones((self.chart_height, self.chart_width, 4), dtype=np.uint8) * 255
        center_x, center_y = self.chart_width // 2, self.chart_height // 2
        radius = min(self.chart_width, self.chart_height) // 2 - 22

        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

        color_remaining = hex_to_rgb(REMAINING_COLOR) + [255]

        for y in range(self.chart_height):
            for x in range(self.chart_width):
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance <= radius:
                    buf[y, x] = color_remaining

        buf = buf.ravel()
        buf = buf.astype(np.uint8)
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.chart_widget.canvas.ask_update()

    def on_diem_danh_updated(self):
        """Gọi khi có điểm danh mới để cập nhật biểu đồ."""
        print("Debug: Gọi on_diem_danh_updated")
        self.update_chart()