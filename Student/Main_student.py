from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from Student.Infor_student import render_view_infor
from Student.Header_student import render_header
from Student.Menu_student import render_menu


class StudentMainScreen(Screen):
    def load_user(self, user):
        self.user = user
        self.clear_widgets()

        layout = MDBoxLayout(orientation='vertical', spacing=0)

        # Header
        header_layout = MDBoxLayout(size_hint_y=None, height="60dp")
        render_header(header_layout, user)
        layout.add_widget(header_layout)

        # Menu đặt ngay dưới header
        menu_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="70dp",
            padding=(10, 5),
            spacing=10
        )
        render_menu(menu_layout, user, self.manager)
        layout.add_widget(menu_layout)

        # Info section phía dưới menu
        info_layout = MDBoxLayout(size_hint_y=1, padding=(10, 5))
        render_view_infor(info_layout, user)
        layout.add_widget(info_layout)

        self.add_widget(layout)