from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.app import MDApp

# Màu sắc
PRIMARY_COLOR = "#2C387E"
BUTTON_COLOR = "#3F51B5"
TEXT_COLOR = "#000000"
HINT_TEXT_COLOR = "Hint"
BUTTON_COLOR_RGBA = "#303F9F"

# Font và kiểu
FONT_TITLE = "H5"
FONT_NORMAL = "Subtitle1"

# Kích thước
WINDOW_WIDTH = 360
WINDOW_HEIGHT = 640
BUTTON_HEIGHT = 56
PADDING = 20
SPACING = 20

class SettingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(SPACING),
            padding=dp(PADDING),
            md_bg_color=[1, 1, 1, 1]
        )

        # Toolbar với nút quay lại
        toolbar = MDTopAppBar(
            title="Cài đặt",
            left_action_items=[["arrow-left", lambda x: self.go_back(x)]],
            md_bg_color=PRIMARY_COLOR,
            size_hint_y=None,
            height=dp(BUTTON_HEIGHT)
        )
        main_layout.add_widget(toolbar)

        # ScrollView cho danh sách cài đặt
        scroll_view = MDScrollView()

        # Nội dung chính
        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(PADDING),
            spacing=dp(SPACING),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))

        # Danh sách cài đặt
        settings_list = MDList()

        # Chức năng đăng xuất
        logout_item = OneLineListItem(
            text="Đăng xuất",
            font_style=FONT_NORMAL,
            on_release=self.logout
        )
        settings_list.add_widget(logout_item)

        # Chức năng đổi mật khẩu
        password_item = OneLineListItem(
            text="Đổi mật khẩu",
            font_style=FONT_NORMAL,
            on_release=self.goto_edit_password
        )
        settings_list.add_widget(password_item)

        # Các chức năng cài đặt khác
        settings_options = [
            "Cài đặt thông báo",
            "Cài đặt ngôn ngữ",
            "Cài đặt bảo mật",
            "Xóa bộ nhớ đệm",
            "Về ứng dụng"
        ]

        for option in settings_options:
            item = OneLineListItem(
                text=option,
                font_style=FONT_NORMAL,
                on_release=lambda x, opt=option: self.on_setting_selected(opt)
            )
            settings_list.add_widget(item)

        content.add_widget(settings_list)
        scroll_view.add_widget(content)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = "student_main"

    def logout(self, instance):
        app = MDApp.get_running_app()
        self.manager.current = "login"

    def goto_edit_password(self, instance):
        self.manager.current = "edit_password"

    def on_setting_selected(self, option):
        print(f"Đã chọn: {option}")