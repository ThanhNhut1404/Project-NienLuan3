from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.toast import toast
from kivy.uix.image import Image

import numpy as np
import cv2
import datetime
import sqlite3
import face_recognition

from Database.Create_db import DB_NAME


class RollCallScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.camera = None
        self.image_widget = None
        self.capture_event = None
        self.known_encodings = []
        self.face_verified = False
        self.qr_data = None
        self.timeout = 20
        self.start_time = None
        self.detector = cv2.QRCodeDetector()

    def on_enter(self):
        self.build_idle_layout()

    def build_idle_layout(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)

        layout.add_widget(MDLabel(
            text="📌 Điểm danh hoạt động",
            halign="center",
            font_style="H5"
        ))

        layout.add_widget(MDLabel(
            text="👤 Hệ thống sẽ nhận diện khuôn mặt và quét mã QR.",
            halign="center",
            theme_text_color="Secondary"
        ))

        start_btn = MDRaisedButton(
            text="▶ BẮT ĐẦU ĐIỂM DANH",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0.6, 0.1, 1),
            text_color="white",
            on_release=self.build_camera_layout
        )
        layout.add_widget(start_btn)

        back_btn = MDFlatButton(
            text="← Quay lại",
            pos_hint={"center_x": 0.5},
            text_color="red",
            on_release=self.go_back_to_main
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def build_camera_layout(self, *args):
        self.clear_widgets()
        self.face_verified = False
        self.qr_data = None
        self.start_time = datetime.datetime.now()

        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        self.image_widget = Image(allow_stretch=True, keep_ratio=True)
        layout.add_widget(self.image_widget)

        stop_btn = MDRaisedButton(
            text="❌ Thoát điểm danh",
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 0, 0, 1),
            on_release=self.stop_roll_call
        )
        layout.add_widget(stop_btn)

        self.add_widget(layout)

        self.set_user(self.user)
        if not self.known_encodings:
            toast("❌ Sinh viên chưa có dữ liệu khuôn mặt.")
            self.build_idle_layout()
            return

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            toast("❌ Không mở được camera.")
            self.build_idle_layout()
            return

        self.capture_event = Clock.schedule_interval(self.update, 1.0 / 30)

    def stop_roll_call(self, *args):
        if self.capture_event:
            self.capture_event.cancel()
        if self.camera:
            self.camera.release()
            self.camera = None

        self.image_widget.texture = None
        self.build_idle_layout()

    def go_back_to_main(self, *args):
        if self.manager:
            self.manager.current = "student_main"

    def set_user(self, user):
        self.user = user
        self.known_encodings = [np.array(enc) for enc in self.user.get("encodings", [])]

    def update(self, dt):
        if not self.camera or not self.camera.isOpened():
            return

        ret, frame = self.camera.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.45)
            if matches.count(True) > 0:
                self.face_verified = True
                break

        if self.face_verified:
            data, bbox, _ = self.detector.detectAndDecode(frame)
            if bbox is not None and data and data.startswith("HOATDONG:"):
                self.qr_data = data.replace("HOATDONG:", "")
                self.finish()
                return

        buf = cv2.flip(rgb, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image_widget.texture = texture

        if (datetime.datetime.now() - self.start_time).total_seconds() > self.timeout:
            self.finish()

    def finish(self):
        if self.capture_event:
            self.capture_event.cancel()
        if self.camera:
            self.camera.release()
            self.camera = None
        self.image_widget.texture = None

        if not self.face_verified:
            toast("❌ Không xác minh được khuôn mặt.")
            self.build_idle_layout()
            return
        if not self.qr_data:
            toast("❌ Không quét được mã QR hợp lệ.")
            self.build_idle_layout()
            return

        self.process_attendance()
        self.build_idle_layout()

    def process_attendance(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT TEN_HD, START_TIME, TIME_OUT, NGAY_TO_CHUC, DIEM_CONG, id_hk
                FROM HOAT_DONG WHERE ID_HD = ?
            ''', (self.qr_data,))
            row = cursor.fetchone()
            if not row:
                toast("❌ Không tìm thấy hoạt động.")
                return

            ten_hd, start_str, end_str, ngay_str, diem_cong, id_hk = row
            start_dt = datetime.datetime.strptime(f"{ngay_str} {start_str}", "%d/%m/%Y %H:%M:%S")
            end_dt = datetime.datetime.strptime(f"{ngay_str} {end_str}", "%d/%m/%Y %H:%M:%S")
            now = datetime.datetime.now()

            if not (start_dt <= now <= end_dt):
                toast(f"⚠️ Hoạt động '{ten_hd}' chưa bắt đầu hoặc đã kết thúc.")
                return

            cursor.execute('''
                SELECT 1 FROM DIEM_DANH_HOAT_DONG
                WHERE id_hoat_dong = ? AND MSSV = ?
            ''', (self.qr_data, self.user["mssv"]))
            if cursor.fetchone():
                toast(f"ℹ️ Bạn đã điểm danh hoạt động '{ten_hd}'.")
                return

            cursor.execute('''
                INSERT INTO DIEM_DANH_HOAT_DONG (id_hoat_dong, MSSV, thoi_gian, diem_cong, id_hk)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.qr_data, self.user["mssv"], now.strftime("%Y-%m-%d %H:%M:%S"), diem_cong, id_hk))

            cursor.execute('''
                UPDATE SINH_VIEN SET TONG_DIEM_HD = IFNULL(TONG_DIEM_HD, 0) + ?
                WHERE MSSV = ?
            ''', (diem_cong, self.user["mssv"]))

            conn.commit()
            toast(f"✅ Điểm danh thành công hoạt động '{ten_hd}'.")

        except Exception as e:
            toast(f"❌ Lỗi: {str(e)}")
        finally:
            conn.close()
