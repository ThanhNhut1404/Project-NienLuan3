from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.app import MDApp
from Student.Login_student import LoginScreen, FaceScanScreen
from Student.Main_student import StudentMainScreen
from Student.Activity_roll_call import RollCallScreen
from Student.View_activity import ViewActivityScreen
from Student.Update_student import UpdateStudentScreen
from Student.Infor_student import ViewInforScreen
from Student.Edit_password import EditPasswordScreen

# Màu sắc
PRIMARY_COLOR = "#2C387E"
ACCENT_COLOR = "#3F51B5"
BACKGROUND_COLOR = "#F5F7FA"
TEXT_COLOR = "#212121"
SECONDARY_TEXT_COLOR = "#757575"
CARD_COLOR = "#FFFFFF"
BUTTON_RADIUS = 12

# Font và kiểu
FONT_TITLE = "H6"
FONT_SUBTITLE = "Subtitle1"
FONT_BODY = "Body1"

# Kích thước
BUTTON_HEIGHT = 56
PADDING = 16
SPACING = 12

class SettingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(SPACING),
            padding=[0, 0, 0, dp(PADDING)],  # Bỏ padding trái-phải, giữ padding dưới
            md_bg_color=BACKGROUND_COLOR,
            size_hint=(1, 1)  # Full screen width and height
        )

        # Toolbar với nút quay lại
        toolbar = MDTopAppBar(
            title="Cài Đặt",
            left_action_items=[["arrow-left", lambda x: self.go_back(x)]],
            md_bg_color=PRIMARY_COLOR,
            specific_text_color="#FFFFFF",
            size_hint=(1, None),  # Full width, fixed height
            height=dp(BUTTON_HEIGHT),
            elevation=0,  # Remove shadow
            pos_hint={"top": 1}
        )
        main_layout.add_widget(toolbar)

        # ScrollView cho danh sách cài đặt
        scroll_view = MDScrollView(
            size_hint=(1, 1)  # Full available space
        )

        # Nội dung chính
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(PADDING), dp(PADDING), dp(PADDING), dp(PADDING)],
            spacing=dp(SPACING),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))

        # Danh sách cài đặt
        settings_list = MDList()

        # Chức năng đăng xuất
        logout_item = OneLineListItem(
            text="Đăng Xuất",
            font_style=FONT_SUBTITLE,
            theme_text_color="Custom",
            text_color=TEXT_COLOR,
            bg_color=CARD_COLOR,
            radius=[BUTTON_RADIUS] * 4,
            size_hint=(1, None),  # Full width
            height=dp(48),
            on_release=self.logout
        )
        settings_list.add_widget(logout_item)

        # Chức năng đổi mật khẩu
        password_item = OneLineListItem(
            text="Đổi Mật Khẩu",
            font_style=FONT_SUBTITLE,
            theme_text_color="Custom",
            text_color=TEXT_COLOR,
            bg_color=CARD_COLOR,
            radius=[BUTTON_RADIUS] * 4,
            size_hint=(1, None),  # Full width
            height=dp(48),
            on_release=self.goto_edit_password
        )
        settings_list.add_widget(password_item)

        # Các chức năng cài đặt khác
        settings_options = [
            "Cài Đặt Thông Báo",
            "Cài Đặt Ngôn Ngữ",
            "Cài Đặt Bảo Mật",
            "Xóa Bộ Nhớ Đệm",
            "Về Ứng Dụng"
        ]

        for option in settings_options:
            item = OneLineListItem(
                text=option,
                font_style=FONT_SUBTITLE,
                theme_text_color="Custom",
                text_color=TEXT_COLOR,
                bg_color=CARD_COLOR,
                radius=[BUTTON_RADIUS] * 4,
                size_hint=(1, None),  # Full width
                height=dp(48),
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
        # Xóa thông tin người dùng
        if hasattr(app, 'user'):
            app.user = None
        # Xóa tất cả màn hình trong ScreenManager
        app.sm.clear_widgets()
        # Tái tạo các màn hình như trong build
        app.sm.add_widget(LoginScreen(name="login"))
        app.sm.add_widget(FaceScanScreen(name="face_scan"))
        app.main_screen = StudentMainScreen(name="student_main")
        app.sm.add_widget(app.main_screen)
        app.roll_call_screen = RollCallScreen(name="roll_call")
        app.sm.add_widget(app.roll_call_screen)
        app.view_activity_screen = ViewActivityScreen(name="view_activity")
        app.sm.add_widget(app.view_activity_screen)
        app.update_student_screen = UpdateStudentScreen(name="update_student")
        app.sm.add_widget(app.update_student_screen)
        app.view_infor_screen = ViewInforScreen(name="view_infor")
        app.sm.add_widget(app.view_infor_screen)
        app.setting_screen = SettingScreen(name="setting")
        app.sm.add_widget(app.setting_screen)
        app.edit_password_screen = EditPasswordScreen(name="edit_password")
        app.sm.add_widget(app.edit_password_screen)
        # Chuyển về màn hình login
        app.sm.current = "login"
        print("Đã đăng xuất và khởi động lại ứng dụng.")

    def goto_edit_password(self, instance):
        self.manager.current = "edit_password"

    def on_setting_selected(self, option):
        print(f"Đã chọn: {option}")