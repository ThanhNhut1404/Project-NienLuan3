from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

def render_header(container, user):
    header = MDBoxLayout(
        orientation='horizontal',
        size_hint_y=None,
        height="50dp",
        md_bg_color="#2C387E",  # Đồng bộ với PRIMARY_COLOR
        padding=(20, 5),
        spacing=10
    )

    title_label = MDLabel(
        text="🎓 HỆ THỐNG ĐIỂM RÈN LUYỆN",
        font_style="H6",
        theme_text_color="Custom",
        text_color="white",
        halign="left"
    )

    greet_label = MDLabel(
        text=f"Xin chào, {user.get('name', 'Sinh viên')}",
        font_style="Caption",
        italic=True,
        theme_text_color="Custom",
        text_color="white",
        halign="right"
    )

    header.add_widget(title_label)
    header.add_widget(greet_label)

    container.add_widget(header)