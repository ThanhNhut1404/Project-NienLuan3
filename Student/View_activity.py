# View_activity.py
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
import sqlite3

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
            spacing=dp(4),
            padding=[dp(4), dp(4), dp(4), dp(4)]
        )

        # — Toolbar —
        toolbar = MDTopAppBar(
            title="Hoạt động đã tham gia",
            elevation=2,
            size_hint_y=None,
            height=dp(44)
        )
        toolbar.left_action_items = [["arrow-left", lambda x: self.back_to_main()]]
        root.add_widget(toolbar)

        # — Button chọn học kỳ —
        self.hk_button = MDRaisedButton(
            text="Chọn HK",
            size_hint=(None, None),
            size=(dp(140), dp(32)),
            pos_hint={"center_x": 0.5},
            on_release=self.open_hk_menu
        )
        root.add_widget(self.hk_button)

        # — Container và DataTable —
        self.container = root
        self.data_table = MDDataTable(
            size_hint=(1, 0.78),
            use_pagination=False,
            column_data=[
                ("STT", dp(18)),
                ("Tên hoạt động", dp(80)),
                ("Cấp", dp(30)),
                ("Loại", dp(30)),
                ("GXN", dp(25)),
                ("Điểm", dp(20)),
            ],
            row_data=[]
        )
        root.add_widget(self.data_table)

        self.add_widget(root)
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
            caller=self.hk_button,
            items=items,
            width_mult=2.5
        )

    def open_hk_menu(self, *args):
        if self.menu:
            self.menu.open()

    def select_hk(self, text):
        self.hk_button.text = text
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
        self.container.remove_widget(self.data_table)
        self.data_table = MDDataTable(
            size_hint=(1, 0.78),
            use_pagination=False,
            column_data=[
                ("STT", dp(18)),
                ("Tên hoạt động", dp(80)),
                ("Cấp", dp(30)),
                ("Loại", dp(30)),
                ("GXN", dp(25)),
                ("Điểm", dp(20)),
            ],
            row_data=rows
        )
        self.container.add_widget(self.data_table)
