from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
import sqlite3
from kivy.graphics import Color, Line
from kivy.clock import Clock

from Database.Create_db import DB_NAME


class ViewActivityScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.hk_button = None
        self.menu = None
        self.data_table = None
        self.container = None

    def set_user(self, user):
        """Gọi từ menu để thiết lập user trước khi vào màn."""
        self.user = user

    def on_enter(self):
        """Mỗi lần chuyển vào màn này, xây dựng lại UI."""
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = MDBoxLayout(
            orientation="vertical",
            spacing=0,
            padding=[0, 0, 0, 0],
            size_hint=(1, 1)  # Đảm bảo layout cha full width
        )

        # — Toolbar —
        toolbar = MDTopAppBar(
            title="Hoạt động đã tham gia",
            elevation=0,
            md_bg_color=(0.17, 0.22, 0.49, 1),
            size_hint_y=None,
            height=dp(44),
            size_hint_x=1  # Make toolbar full width
        )
        toolbar.left_action_items = [["arrow-left", lambda x: self.back_to_main()]]
        root.add_widget(toolbar)

        # — Container và DataTable —
        self.container = root

        # Tạo một layout ngang cho nút chọn học kỳ kiểu label + icon
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDIconButton
        from kivy.uix.boxlayout import BoxLayout
        frame_layout = BoxLayout(orientation="horizontal", size_hint=(None, None), height=dp(40), width=dp(300), padding=[0,0,0,0], spacing=0)
        self.hk_label = MDLabel(
            text="Chọn học kỳ",
            font_style="Subtitle1",
            size_hint=(None, None),
            halign="left",
            valign="middle",
            theme_text_color="Primary",
            height=dp(32),
            width=dp(250),
            shorten=False,
            max_lines=1
        )
        self.hk_icon = MDIconButton(
            icon="chevron-down",
            size_hint=(None, None),
            height=dp(32),
            width=dp(32),
            on_release=self.open_hk_menu
        )
        # Khi bấm vào label cũng mở menu
        self.hk_label.bind(on_touch_down=lambda instance, touch: self.open_hk_menu() if self.hk_label.collide_point(*touch.pos) else None)
        frame_layout.add_widget(self.hk_label)
        frame_layout.add_widget(self.hk_icon)
        # Thêm lại frame_layout và bảng vào layout cha
        self.box = BoxLayout(orientation="vertical", size_hint_x=1, spacing=0, padding=[0,0,0,0])
        self.box.add_widget(frame_layout)
        self.data_table = MDDataTable(
            size_hint=(1, 0.78),
            use_pagination=False,
            elevation=0,
            column_data=[
                ("STT", dp(15), "center"),
                ("Tên hoạt động", dp(90), "left"),
                ("Cấp hoạt động", dp(35), "center"),
                ("Loại hoạt động", dp(35), "center"),
                ("GXN", dp(35), "center"),
                ("Điểm", dp(35), "center"),
            ],
            row_data=[]
        )
        self.box.add_widget(self.data_table)
        root.add_widget(self.box)

        self.add_widget(root)

        # Tải học kỳ để hiển thị lên menu
        self.load_hk_items()

    def back_to_main(self):
        self.manager.current = "student_main"

    def load_hk_items(self):
        """Tải học kỳ từ DB, tạo dropdown menu."""
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
            rows = cur.fetchall()

        items = []
        for id_hk, name, year in rows:
            label = f"{id_hk} - {name} ({year})"
            items.append({
                "viewclass": "OneLineListItem",
                "text": label,
                "height": dp(32),
                "on_release": lambda x=label: self.select_hk(x)
            })
            self.menu = MDDropdownMenu(
                caller=self.hk_icon,  # Đổi caller thành icon để menu hiện đúng
                items=items,
                width_mult=2.5
            )

    def open_hk_menu(self, *args):
        if self.menu:
            self.menu.open()

    def select_hk(self, text):
        self.hk_label.text = text
        self.hk_label.shorten = False  # Hiển thị đủ chữ, không cắt
        self.hk_label.max_lines = 1
        self.menu.dismiss()
        self.load_activities(text)


    def load_activities(self, hk_str):
        """Đọc DIEM_DANH_HOAT_DONG, tính điểm và hiển thị lại DataTable."""
        if not self.user:
            return
        mssv = self.user["mssv"]
        id_hk = int(hk_str.split(" - ")[0])

        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            # đảm bảo bảng tổng điểm tồn tại
            cur.execute('''
                    CREATE TABLE IF NOT EXISTS TONG_DIEM_HK (
                        ID_SV TEXT, ID_HK INTEGER, TONG_DIEM INTEGER,
                        PRIMARY KEY(ID_SV, ID_HK)
                    )
                ''')

            cur.execute('''
                    SELECT hd.ID_HD, hd.TEN_HD, hd.CAP_HD, hd.CATEGORY_HD, hd.CO_XAC_NHAN
                    FROM DIEM_DANH_HOAT_DONG dd
                    JOIN HOAT_DONG hd ON dd.ID_HOAT_DONG = hd.ID_HD
                    WHERE dd.MSSV=? AND dd.ID_HK=?
                ''', (mssv, id_hk))
            activities = cur.fetchall()

            # logic tính điểm
            count_loai = {"Tình nguyện": False, "Hội nhập": False}
            max_cap = {"Chi hội": 2, "Liên chi": 3, "Trường": 2}
            count_cap = {"Chi hội": 0, "Liên chi": 0, "Trường": 0}
            used_gxn = False
            total = 0
            rows = []

            for i, (id_hd, ten, cap, loai, gxn) in enumerate(activities, 1):
                diem = 0
                # Loại
                if loai in count_loai and not count_loai[loai]:
                    diem += 4 if loai == "Tình nguyện" else 3
                    count_loai[loai] = True
                # Cấp
                if cap in count_cap and count_cap[cap] < max_cap[cap]:
                    diem += 2 if cap == "Trường" else 1
                    count_cap[cap] += 1
                # Giấy xác nhận
                if str(gxn).strip().lower() == "có" and not used_gxn:
                    diem += 4
                    used_gxn = True

                total += diem
                # cắt ngắn tên nếu quá dài
                display_ten = ten if len(ten) <= 20 else ten[:17] + "..."
                rows.append([str(i), display_ten, cap, loai, str(gxn), str(diem)])

                cur.execute('''
                        UPDATE DIEM_DANH_HOAT_DONG
                        SET diem_cong=?
                        WHERE MSSV=? AND ID_HOAT_DONG=? AND ID_HK=?
                    ''', (diem, mssv, id_hd, id_hk))

            # lưu tổng điểm HK
            cur.execute('''
                    INSERT OR REPLACE INTO TONG_DIEM_HK(ID_SV,ID_HK,TONG_DIEM)
                    VALUES(?,?,?)
                ''', (mssv, id_hk, total))
            # thêm dòng tổng điểm
            rows.append(["", "", "", "", "Tổng điểm:", str(total)])

            # xoá DataTable cũ, tạo và add lại
            self.box.remove_widget(self.data_table)
            self.data_table = MDDataTable(
                size_hint=(1, 0.78),
                use_pagination=False,
                elevation=0,
                column_data=[
                    ("STT", dp(15), "center", "left"),
                    ("Tên hoạt động", dp(90), "center", "left"),  # Tiêu đề và nội dung cột tên hoạt động đều canh giữa
                    ("Cấp hoạt động", dp(35), "center", "center"),
                    ("Loại hoạt động", dp(35), "center", "center"),
                    ("GXN", dp(35), "center", "center"),
                    ("Điểm", dp(35), "center", "center"),
                ],
                row_data=rows
            )
            self.box.add_widget(self.data_table)
