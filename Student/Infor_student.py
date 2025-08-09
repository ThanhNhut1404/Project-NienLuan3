from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
import os
from PIL import Image as PILImage

# Màu sắc và kích thước từ cấu hình
PRIMARY_COLOR = "#2C387E"
BUTTON_COLOR = "#3F51B5"
TEXT_COLOR = "#000000"
BUTTON_COLOR_RGBA = "#303F9F"
FONT_TITLE = "H5"
FONT_NORMAL = "Subtitle1"
WINDOW_WIDTH = 360
WINDOW_HEIGHT = 640
BUTTON_HEIGHT = 56
PADDING = 20
SPACING = 20

def render_view_infor(container, user):
    scroll = MDScrollView()

    outer = MDBoxLayout(
        orientation='vertical',
        padding=dp(PADDING),
        spacing=dp(SPACING * 2),
        size_hint_y=None
    )
    outer.bind(minimum_height=outer.setter('height'))
    scroll.add_widget(outer)

    # THÔNG TIN
    title = MDLabel(
        text="Thông tin sinh viên",
        font_style=FONT_TITLE,
        theme_text_color="Custom",
        text_color=TEXT_COLOR,
        bold=True,
        halign="center",
        size_hint_y=None,
        height=dp(40)
    )
    outer.add_widget(title)

    # AVATAR
    avatar_filename = user.get("img", "default_avatar.png")
    image_path = os.path.join("assets", avatar_filename)
    print(f"Debug - Kiểm tra image_path: {image_path}")
    if not os.path.exists(image_path):
        print(f"Debug - Không tìm thấy {image_path}, sử dụng ảnh mặc định")
        image_path = os.path.join("assets", "default_avatar.png")
        if not os.path.exists(image_path):
            print(f"Debug - Tạo ảnh mặc định tại {image_path}")
            if not os.path.exists("assets"):
                os.makedirs("assets")
            PILImage.new("RGB", (100, 100), color=(200, 200, 200)).save(image_path)

    avatar_card = MDCard(
        size_hint=(None, None),
        size=(dp(100), dp(100)),
        radius=[dp(50)],
        md_bg_color=[1, 1, 1, 1],
        pos_hint={"center_x": 0.5}
    )
    avatar = Image(
        source=image_path,
        size_hint=(1, 1),
        allow_stretch=True,
        keep_ratio=False,
        pos_hint={"center_x": 0.5, "center_y": 0.5}
    )
    avatar_card.add_widget(avatar)
    outer.add_widget(avatar_card)

    # THÔNG TIN KHÁC
    info_card = MDCard(
        orientation='vertical',
        padding=(dp(3), dp(9)),
        spacing=dp(5),
        size_hint=(1, None)
    )
    info_card.bind(minimum_height=info_card.setter('height'))
    outer.add_widget(info_card)

    def add_pair(label, value):
        row = MDBoxLayout(
            orientation='horizontal',
            padding=(dp(2), 0),
            spacing=dp(4),
            size_hint_y=None,
            height=dp(25)
        )
        row.add_widget(
            MDLabel(
                text=label,
                font_style=FONT_NORMAL,
                halign="left",
                size_hint_x=None,
                width=dp(90),
                theme_text_color="Custom",
                text_color=TEXT_COLOR
            )
        )
        row.add_widget(
            MDLabel(
                text=value,
                font_style=FONT_NORMAL,
                theme_text_color="Custom",
                text_color=(0.2, 0.5, 0.9, 1),
                bold=True,
                halign="left",
                size_hint_x=1
            )
        )
        info_card.add_widget(row)

    add_pair("MSSV:", user.get("mssv", ""))
    add_pair("Họ tên:", user.get("name", ""))
    add_pair("Lớp:", user.get("class", ""))
    add_pair("Giới tính:", "Nam" if user.get("sex") == 1 else "Nữ")
    add_pair("Ngày sinh:", user.get("date", ""))
    add_pair("Địa chỉ:", user.get("address", ""))
    add_pair("Email:", user.get("email", ""))
    add_pair("SĐT:", user.get("phone", ""))

    container.add_widget(scroll)

class ViewInforScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = {}
        self.info_container = None

    def load_user(self, user_data):
        self.user = user_data
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        root = FloatLayout()  # root để chứa main content + FAB nổi

        # Nội dung chính (toolbar + scroll content)
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=0,
            padding=0,
            md_bg_color=[1, 1, 1, 1],
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        # Thanh tiêu đề
        toolbar = MDTopAppBar(
            title="Thông tin sinh viên",
            left_action_items=[["arrow-left", lambda x: self.go_back(x)]],
            md_bg_color=PRIMARY_COLOR,
            size_hint_y=None,
            height=dp(BUTTON_HEIGHT),
            elevation=0
        )
        main_layout.add_widget(toolbar)

        # vùng chứa nội dung
        self.info_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint=(1, 1)
        )
        render_view_infor(self.info_container, self.user)
        main_layout.add_widget(self.info_container)

        # thêm main_layout vào root (nằm phía dưới)
        root.add_widget(main_layout)

        # Nút cập nhật — nằm nổi lên trên nội dung nhờ FloatLayout
        update_btn = MDFloatingActionButton(
            icon="pencil",
            md_bg_color=BUTTON_COLOR,
            size_hint=(None, None),
            size=(dp(55), dp(55)),  # to hơn nếu cần
            pos_hint={"center_x": 0.5, "y": 0.02}  # tăng y để "cao lên" (0.08 ~ hơi trên đáy)
        )
        update_btn.bind(on_release=self.go_to_update)
        root.add_widget(update_btn)

        self.add_widget(root)

    def go_back(self, instance):
        self.manager.current = "student_main"

    def go_to_update(self, instance):
        update_screen = self.manager.get_screen("update_student")
        update_screen.load_user(self.user)
        self.manager.current = "update_student"