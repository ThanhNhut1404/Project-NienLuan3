from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Student.Login_student import LoginScreen, FaceScanScreen
from Student.Main_student import StudentMainScreen
from Student.Activity_roll_call import RollCallScreen
from Student.View_activity import ViewActivityScreen
from Database.Create_db import get_all_sinh_vien
from Student.Update_student import UpdateStudentScreen
from Student.Infor_student import ViewInforScreen
from Student.Setting import SettingScreen
from Student.Edit_password import EditPasswordScreen  # Import màn hình mới

class StudentApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.sm = ScreenManager()

        # Đăng nhập và quét khuôn mặt
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(FaceScanScreen(name="face_scan"))

        # Màn hình chính
        self.main_screen = StudentMainScreen(name="student_main")
        self.sm.add_widget(self.main_screen)

        # Màn hình điểm danh
        self.roll_call_screen = RollCallScreen(name="roll_call")
        self.sm.add_widget(self.roll_call_screen)

        # Màn hình xem hoạt động
        self.view_activity_screen = ViewActivityScreen(name="view_activity")
        self.sm.add_widget(self.view_activity_screen)

        # Màn hình cập nhật thông tin
        self.update_student_screen = UpdateStudentScreen(name="update_student")
        self.sm.add_widget(self.update_student_screen)

        # Màn hình xem thông tin sinh viên
        self.view_infor_screen = ViewInforScreen(name="view_infor")
        self.sm.add_widget(self.view_infor_screen)

        # Màn hình cài đặt
        self.setting_screen = SettingScreen(name="setting")
        self.sm.add_widget(self.setting_screen)

        # Màn hình đổi mật khẩu
        self.edit_password_screen = EditPasswordScreen(name="edit_password")
        self.sm.add_widget(self.edit_password_screen)

        return self.sm

    def on_start(self):
        # Đảm bảo màn hình khởi đầu là login
        self.sm.current = "login"

if __name__ == "__main__":
    StudentApp().run()