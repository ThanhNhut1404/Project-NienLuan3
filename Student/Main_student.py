from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from Student.Infor_student import render_view_infor
from Student.Header_student import render_header
from Student.Menu_student import render_menu
from Student.Activity_notification import ActivityNotification
from Student.Point_chart import PointChart

class StudentMainScreen(Screen):
    def load_user(self, user):
        self.user = user
        self.clear_widgets()

        # Layout chính
        main_layout = MDBoxLayout(orientation='vertical')

        # Header nằm sát trên cùng
        header_layout = MDBoxLayout(size_hint_y=None, height="60dp")
        render_header(header_layout, user)
        main_layout.add_widget(header_layout)

        # ScrollView cho nội dung giữa
        scroll_layout = MDScrollView()
        content_layout = MDBoxLayout(orientation='vertical', padding="10dp", spacing="10dp", size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        # Thêm hình ảnh Logo_login.png
        logo_image = Image(
            source="Image/Logo_login.png",
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x': 0.5}
        )
        content_layout.add_widget(logo_image)

        # Thêm thông báo hoạt động
        notification = ActivityNotification(size_hint_y=None, height=200)  # Chiều cao cố định
        content_layout.add_widget(notification)

        # Thêm biểu đồ điểm
        point_chart = PointChart(user=user, size_hint_y=None, height=300)  # Chiều cao cố định
        content_layout.add_widget(point_chart)

        # Thêm thông tin sinh viên
        render_view_infor(content_layout, user)

        scroll_layout.add_widget(content_layout)
        main_layout.add_widget(scroll_layout)

        # Menu nằm sát dưới cùng
        menu_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="70dp",
            padding=(10, 5),
            spacing=10
        )
        render_menu(menu_layout, user, self.manager)
        main_layout.add_widget(menu_layout)

        self.add_widget(main_layout)