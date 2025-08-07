from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior


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
        roll_call_screen = screen_manager.get_screen('roll_call')
        roll_call_screen.set_user(user)
        screen_manager.current = 'roll_call'

    def goto_activity(*args):
        screen = screen_manager.get_screen("view_activity")
        screen.set_user(user)
        screen_manager.current = "view_activity"

    menu_layout.clear_widgets()
    menu_layout.add_widget(MenuButton("home", "Trang chủ", goto_home))
    menu_layout.add_widget(MenuButton("account", "Thông tin", goto_infor))
    menu_layout.add_widget(MenuButton("calendar", "Điểm danh", goto_roll_call))
    menu_layout.add_widget(MenuButton("clipboard-list", "Hoạt động", goto_activity))
