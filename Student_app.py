from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Student.Login_student import LoginScreen, FaceScanScreen
from Student.Main_student import StudentMainScreen
from Student.Activity_roll_call import RollCallScreen
from Student.View_activity import ViewActivityScreen
from Database.Create_db import get_all_sinh_vien


class StudentApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.sm = ScreenManager()

        # Đăng nhập và quét khuôn mặt
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(FaceScanScreen(name="face_scan"))

        #Lấy user mẫu (sau này truyền từ login hoặc face scan)
        mssv = "123"  # Giả lập MSSV
        all_sv = get_all_sinh_vien()
        user = next((sv for sv in all_sv if sv["mssv"] == mssv), None)

        if not user:
            print("❌ Không tìm thấy sinh viên với MSSV:", mssv)
            user = {"mssv": "Unknown", "name": "Ẩn danh"}

        #Màn hình chính
        self.main_screen = StudentMainScreen(name="student_main")
        self.main_screen.load_user(user)
        self.sm.add_widget(self.main_screen)

        #Màn hình điểm danh
        self.roll_call_screen = RollCallScreen(name="roll_call")
        self.roll_call_screen.set_user(user)
        self.sm.add_widget(self.roll_call_screen)

        #Màn hình xem hoạt động
        self.view_activity_screen = ViewActivityScreen(name="view_activity")
        self.view_activity_screen.user = user  # Gán sau khi khởi tạo
        self.sm.add_widget(self.view_activity_screen)

        return self.sm


if __name__ == "__main__":
    StudentApp().run()
