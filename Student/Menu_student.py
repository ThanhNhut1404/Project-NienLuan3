from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.utils import get_color_from_hex


class MenuButton(ButtonBehavior, MDBoxLayout):
    def __init__(self, icon, text, on_press_action, **kwargs):
        # spacing âm nhiều hơn để label sát icon
        super().__init__(orientation='vertical', spacing=-dp(6), **kwargs)
        self.padding = (0, dp(1))  # giảm padding top/bottom
        self.size_hint_x = None
        self.width = dp(72)
        self.pos_hint = {"center_x": 0.5}

        # icon
        self.icon_btn = MDIconButton(
            icon=icon,
            theme_icon_color="Custom",
            icon_color=[0, 0, 1, 1],
            size_hint=(None, None),
            size=(dp(26), dp(26)),  # nhỏ hơn chút để label gần hơn
            pos_hint={"center_x": 0.5},
        )
        self.icon_btn.bind(on_release=on_press_action)
        self.add_widget(self.icon_btn)

        # label
        self.label = MDLabel(
            text=text,
            halign="center",
            font_style="Caption",
            size_hint=(1, None),
            height=dp(14),
            valign="middle",
        )
        self.label.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, None)))
        self.add_widget(self.label)


def render_menu(menu_layout, user, screen_manager):
    def goto_home(*args):
        screen_manager.current = 'student_main'

    def goto_infor(*args):
        if user:
            app = MDApp.get_running_app()
            view_screen = app.sm.get_screen("view_infor")
            view_screen.load_user(user)
            app.sm.current = "view_infor"
        screen_manager.current = "view_infor"

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

    def goto_setting(*args):
        screen_manager.current = "setting"

    # Xóa widget cũ
    menu_layout.clear_widgets()

    # Layout cha (full width, nền xám)
    wrapper = MDBoxLayout(
        size_hint_x=1,
        size_hint_y=None,
        height=dp(50),
        padding=(0, 0, 0, 0),
        spacing=0,
        md_bg_color=get_color_from_hex("#F0F0F0")
    )

    # Layout con (chỉ rộng bằng tổng nút, canh giữa)
    inner_layout = MDBoxLayout(
        size_hint_x=None,
        size_hint_y=None,
        height=dp(50),
        spacing=dp(10),
        pos_hint={"center_x": 0.5}
    )

    # Thêm các nút menu vào inner_layout
    wrapper.add_widget(MenuButton("account", "Thông tin", goto_infor))
    wrapper.add_widget(MenuButton("calendar", "Điểm danh", goto_roll_call))
    wrapper.add_widget(MenuButton("clipboard-list", "Hoạt động", goto_activity))
    wrapper.add_widget(MenuButton("cog", "Cài đặt", goto_setting))

    # Tính width chính xác cho inner_layout
    inner_layout.width = sum(child.width for child in inner_layout.children) + inner_layout.spacing * (len(inner_layout.children) - 1)

    # Gắn vào layout cha
    wrapper.add_widget(inner_layout)

    # Gắn vào menu_layout
    menu_layout.add_widget(wrapper)

    if not user:
        print("Debug - user không hợp lệ hoặc rỗng khi render menu")