from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
import os

def render_view_infor(container, user):
    # KHÔNG clear container, chỉ gắn widget mới
    scroll = MDScrollView()

    outer = MDBoxLayout(
        orientation='vertical',
        padding=(10, 15),
        spacing=12,
        size_hint_y=None
    )
    outer.bind(minimum_height=outer.setter('height'))
    scroll.add_widget(outer)

    # KHUNG CHÍNH
    main_box = MDBoxLayout(
        orientation='horizontal',
        spacing=10,
        size_hint_y=None,
        height="180dp"
    )
    outer.add_widget(main_box)

    # AVATAR
    image_path = user.get("img", "") or "avatar.png"
    if not os.path.exists(image_path):
        image_path = "avatar.png"

    avatar_card = MDCard(
        size_hint=(None, None),
        size=("100dp", "140dp"),
        radius=[12],
        elevation=4,
        md_bg_color="white"
    )
    avatar = Image(source=image_path, allow_stretch=True, keep_ratio=True)
    avatar_card.add_widget(avatar)
    main_box.add_widget(avatar_card)

    # THÔNG TIN
    info_box = MDBoxLayout(
        orientation='vertical',
        spacing=6,
        padding=(0, 5),
        size_hint_x=0.6,
        size_hint_y=None
    )
    info_box.bind(minimum_height=info_box.setter('height'))
    main_box.add_widget(info_box)

    title = MDLabel(
        text="📄 Thông tin sinh viên",
        font_style="Subtitle1",
        theme_text_color="Custom",
        text_color="#00897B",
        halign="left",
        size_hint_y=None,
        height="24dp"
    )
    info_box.add_widget(title)

    def add_pair(label1, value1, label2, value2):
        row = MDBoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height="24dp")

        left = MDBoxLayout(orientation='horizontal', spacing=2, size_hint_x=0.5)
        left.add_widget(MDLabel(text=label1, font_style="Caption", halign="left", size_hint_x=None, width=60))
        left.add_widget(MDLabel(text=value1, font_style="Caption", theme_text_color="Custom", text_color="#00897B"))

        right = MDBoxLayout(orientation='horizontal', spacing=2, size_hint_x=0.5)
        right.add_widget(MDLabel(text=label2, font_style="Caption", halign="left", size_hint_x=None, width=60))
        right.add_widget(MDLabel(text=value2, font_style="Caption", theme_text_color="Custom", text_color="#00897B"))

        row.add_widget(left)
        row.add_widget(right)
        outer.add_widget(row)

    add_pair("👨‍🎓 MSSV:", user.get("mssv", ""), "🏠 Địa chỉ:", user.get("address", ""))
    add_pair("🧑 Họ tên:", user.get("name", ""), "🎓 Lớp:", user.get("class", ""))
    add_pair("👤 Giới tính:", "Nam" if user.get("sex") == 1 else "Nữ", "📧 Email:", user.get("email", ""))
    add_pair("🎂 Ngày sinh:", user.get("date", ""), "📞 SĐT:", user.get("phone", ""))

    container.add_widget(scroll)