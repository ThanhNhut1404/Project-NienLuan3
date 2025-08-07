from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp

class MenuButton(ButtonBehavior, MDBoxLayout):
    def __init__(self, icon, text, on_press_action, **kwargs):
        super().__init__(orientation='vertical', spacing=4, **kwargs)
        self.padding = (0, 5)
        self.size_hint = (None, 1)
        self.width = "80dp"

        self.icon_btn = MDIconButton(
            icon=icon,
            theme_icon_color="Custom",
            icon_color="blue"
        )
        self.icon_btn.bind(on_release=on_press_action)
        self.add_widget(self.icon_btn)

        self.label = MDLabel(
            text=text,
            halign="center",
            font_style="Caption"
        )
        self.add_widget(self.label)

def render_menu(menu_layout, user, screen_manager):
    def goto_home(*args):
        screen_manager.current = 'student_main'

    def goto_infor(*args):
        screen_manager.current = 'view_infor'

    def goto_roll_call(*args):
        if user:
            roll_call_screen = screen_manager.get_screen('roll_call')
            roll_call_screen.set_user(user)
        screen_manager.current = 'roll_call'

    def goto_activity(*args):
        if user:
            screen = screen_manager.get_screen("view_activity")
            screen.set_user(user)
        screen_manager.current = "view_activity"

    def goto_update_student(*args):
        if user:
            app = MDApp.get_running_app()
            update_screen = app.update_student_screen
            update_screen.load_user(user)  # Sử dụng user được truyền vào thay vì app.main_screen.user
        app.sm.current = "update_student"

    menu_layout.clear_widgets()
    menu_layout.add_widget(MenuButton("home", "Trang chủ", goto_home))
    menu_layout.add_widget(MenuButton("account", "Thông tin", goto_infor))
    menu_layout.add_widget(MenuButton("calendar", "Điểm danh", goto_roll_call))
    menu_layout.add_widget(MenuButton("clipboard-list", "Hoạt động", goto_activity))
    menu_layout.add_widget(MenuButton("account-edit", "Cập nhật", goto_update_student))

    if not user:
        print("Debug - user không hợp lệ hoặc rỗng khi render menu")