from kivy.core.window import Window
from kivy.metrics import dp
from Styles.Styles_student import (
    WINDOW_WIDTH, WINDOW_HEIGHT, PADDING, SPACING,
    FONT_TITLE, BUTTON_HEIGHT, HINT_TEXT_COLOR, BUTTON_COLOR_RGBA
)

Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.scrollview import ScrollView
import cv2
from kivy.metrics import sp
import face_recognition
import hashlib
import numpy as np
from Database.Create_db import get_all_sinh_vien

class CameraFeed(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = None
        self.current_image = None
        self.clock_event = None
        self.texture_obj = None

    def start_camera(self):
        try:
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            if not self.capture.isOpened():
                raise Exception("Không mở được camera")
            self.clock_event = Clock.schedule_interval(self.update, 1/15)
        except Exception as e:
            toast(f"Lỗi camera: {e}")
            MDApp.get_running_app().stop()

    def stop_camera(self):
        if self.clock_event:
            Clock.unschedule(self.clock_event)
        if self.capture:
            self.capture.release()

    def update(self, dt):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                buf = rgb.tobytes()
                h, w = rgb.shape[:2]
                if not self.texture_obj:
                    self.texture_obj = Texture.create(size=(w, h), colorfmt='rgb')
                    self.texture_obj.flip_vertical()
                self.texture_obj.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.texture = self.texture_obj
                self.current_image = rgb

    def get_encoding(self):
        if self.current_image is not None:
            boxes = face_recognition.face_locations(self.current_image)
            if len(boxes) == 1:
                return face_recognition.face_encodings(self.current_image, boxes)[0]
        return None

class LineSeparator(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.7, 0.7, 0.7, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = MDBoxLayout(orientation='vertical')

        scroll = ScrollView()
        container = MDBoxLayout(
            orientation='vertical',
            padding=[PADDING, PADDING, PADDING, PADDING],
            spacing=SPACING,
            size_hint_y=None,
        )
        container.bind(minimum_height=container.setter('height'))

        logo = Image(
            source="Image/Logo_login.png",
            size_hint=(1, None),
            height=dp(120),
            fit_mode="contain"
        )
        container.add_widget(logo)

        # Title 'ĐĂNG NHẬP'
        container.add_widget(MDLabel(
            text='ĐĂNG NHẬP',
            halign='center',
            font_style='H5',
            bold=True,
            theme_text_color='Custom',
            text_color=[0, 0, 0, 1],
            size_hint_y=None,
            height=dp(40)
        ))

        mssv_box = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=80,
            padding=[10, 10, 10, 10],
            md_bg_color=(0.85, 0.85, 0.85, 0.3),
            radius=[10, 10, 10, 10]
        )
        mssv_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        self.mssv_input = MDTextField(hint_text='Mã số sinh viên', size_hint=(1, None), height=60)
        mssv_anchor.add_widget(self.mssv_input)
        mssv_box.add_widget(mssv_anchor)

        pass_box = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=80,
            padding=[10, 10, 10, 10],
            md_bg_color=(0.85, 0.85, 0.85, 0.3),
            radius=[10, 10, 10, 10]
        )
        pass_layout = MDRelativeLayout(size_hint_y=None, height=60)
        self.pass_input = MDTextField(hint_text='Mật khẩu', password=True, size_hint=(1, None), height=60, pos_hint={'center_y': 0.5})
        pass_layout.add_widget(self.pass_input)
        self.eye_button = MDIconButton(icon='eye-off', pos_hint={'center_y': 0.5}, theme_icon_color="Hint", on_release=self.toggle_password_visibility)
        self.eye_button.pos_hint = {"right": 1, "center_y": 0.5}
        pass_layout.add_widget(self.eye_button)
        pass_box.add_widget(pass_layout)

        container.add_widget(mssv_box)
        container.add_widget(pass_box)

        self.message_label = MDLabel(
            text='',
            halign='center',
            theme_text_color='Custom',
            text_color=(1, 0, 0, 1),  # Mặc định màu đỏ
            font_style='Subtitle2'
        )
        container.add_widget(self.message_label)

        login_btn = MDRaisedButton(
            text='ĐĂNG NHẬP',
            on_release=self.login_by_account,
            size_hint=(1, None),
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            md_bg_color=[0.0, 0.6, 0.3, 1],
            font_style="H6",
        )
        login_btn.font_size = sp(13)
        container.add_widget(login_btn)

        separator_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=10)
        left_line = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(0.4, None), height=30)
        left_line.add_widget(LineSeparator(size_hint=(1, None), height=1))
        separator_layout.add_widget(left_line)
        or_label_container = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(None, None), size=(60, 30))
        or_label = MDLabel(text="Hoặc", halign="center", theme_text_color=HINT_TEXT_COLOR, size_hint=(None, None), size=(60, 20))
        or_label_container.add_widget(or_label)
        separator_layout.add_widget(or_label_container)
        right_line = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(0.4, None), height=30)
        right_line.add_widget(LineSeparator(size_hint=(1, None), height=1))
        separator_layout.add_widget(right_line)
        container.add_widget(separator_layout)

        face_btn = MDRaisedButton(
            text='ĐĂNG NHẬP VỚI KHUÔN MẶT',
            on_release=self.go_to_face_scan,
            size_hint=(1, None),
            height=BUTTON_HEIGHT,
            md_bg_color=[1, 0.4, 0.3, 1],
            font_style="H6",
        )
        face_btn.font_size = sp(13)
        container.add_widget(face_btn)

        scroll.add_widget(container)
        self.add_widget(scroll)

        # Footer fixed
        footer = MDBoxLayout(
            orientation='vertical', size_hint_y=None, height=dp(80), padding=[PADDING, 0, PADDING, dp(10)], spacing=dp(5)
        )
        footer.add_widget(Widget())  # spacer
        footer.add_widget(MDLabel(text='Tiếng Việt', halign='center', theme_text_color='Primary'))
        footer.add_widget(MDLabel(text='v1.0.2 (136)', halign='center', theme_text_color='Hint'))
        root.add_widget(footer)

        self.add_widget(root)

    def toggle_password_visibility(self, *args):
        self.pass_input.password = not self.pass_input.password
        self.eye_button.icon = 'eye' if not self.pass_input.password else 'eye-off'

    def login_by_account(self, *args):
        mssv = self.mssv_input.text.strip()
        pwd = self.pass_input.text.strip()

        if not mssv or not pwd:
            self.message_label.text = 'Vui lòng nhập MSSV và mật khẩu'
            self.message_label.text_color = (1, 0, 0, 1)  # đỏ
            return

        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        for user in get_all_sinh_vien():
            if user['mssv'] == mssv and user['password'] == hashed:
                self.message_label.text = 'Đăng nhập thành công'
                self.message_label.text_color = (0, 0.7, 0.2, 1)  # Xanh lá

                def switch_screen(dt):
                    app = MDApp.get_running_app()
                    screen = app.sm.get_screen('student_main')
                    screen.load_user(user)
                    app.sm.current = 'student_main'

                Clock.schedule_once(switch_screen, 0.5)  # đợi 0.5 giây trước khi chuyển

                return

        self.message_label.text = 'MSSV hoặc mật khẩu không đúng'
        self.message_label.text_color = (1, 0, 0, 1)  # đỏ

    def go_to_face_scan(self, *args):
        app = MDApp.get_running_app()
        face_screen = app.sm.get_screen('face_scan')
        face_screen.next_screen = 'student_main'
        app.sm.current = 'face_scan'



class FaceScanScreen(MDScreen):
    def __init__(self, next_screen='student_main', **kwargs):
        super().__init__(**kwargs)
        self.next_screen = next_screen
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(MDLabel(text='📷 Quét khuôn mặt để đăng nhập', halign='center', font_style=FONT_TITLE))
        self.camera = CameraFeed()
        layout.add_widget(self.camera)
        layout.add_widget(MDRaisedButton(text='🔍 Kiểm tra khuôn mặt', on_release=self.verify_face))
        layout.add_widget(MDRaisedButton(text='⬅️ Quay về', on_release=self.go_back))
        scroll = ScrollView()
        scroll.add_widget(layout)
        self.add_widget(scroll)

    def on_enter(self):
        self.camera.start_camera()

    def on_leave(self):
        self.camera.stop_camera()

    def verify_face(self, *args):
        encoding = self.camera.get_encoding()
        if encoding is None:
            toast('❌ Không thấy khuôn mặt hoặc quá nhiều khuôn mặt')
            return
        for user in get_all_sinh_vien():
            for enc in user.get('encodings', []):
                arr = np.array(eval(enc)) if isinstance(enc, str) else enc
                match = face_recognition.compare_faces([arr], encoding, tolerance=0.4)[0]
                if match:
                    toast(f'✅ Xin chào {user["mssv"]}')
                    self.camera.stop_camera()
                    app = MDApp.get_running_app()
                    screen = app.sm.get_screen(self.next_screen)
                    if hasattr(screen, 'load_user'):
                        screen.load_user(user)
                    if hasattr(screen, 'set_user'):
                        screen.set_user(user)
                    app.sm.current = self.next_screen
                    return
        toast('❌ Không tìm thấy khuôn mặt phù hợp')

    def go_back(self, *args):
        MDApp.get_running_app().sm.current = 'login'