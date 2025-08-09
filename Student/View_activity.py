from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
import sqlite3
from kivy.clock import Clock

from Database.Create_db import DB_NAME

class ViewActivityScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.selected_hk = None
        self.hk_spinner = None
        self.data_table = None
        self.scroll_view = None
        self.total_label = None
        self.point_chart = None
        self.debug_log = []  # Để lưu thông tin kiểm tra lỗi

    def set_user(self, user):
        self.user = user

    def set_point_chart(self, point_chart):
        self.point_chart = point_chart

    def on_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = MDBoxLayout(
            orientation="vertical",
            spacing=0,
            padding=[0, 0, 0, 0],
            size_hint=(1, 1)
        )

        # Toolbar
        toolbar = MDTopAppBar(
            title="Hoạt động đã tham gia",
            elevation=0,
            md_bg_color=(0.17, 0.22, 0.49, 1),
            size_hint_y=None,
            height=dp(44),
            size_hint_x=1
        )
        toolbar.left_action_items = [["arrow-left", lambda x: self.back_to_main()]]
        root.add_widget(toolbar)

        self.box = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            spacing=dp(8),
            padding=[dp(8), dp(8), dp(8), dp(8)]
        )

        self.hk_spinner = Spinner(
            text="Vui lòng chọn học kỳ",
            values=[],
            size_hint=(1, None),
            height=dp(35),
            background_color=(0.17, 0.22, 0.49, 1),
            color=(1, 1, 1, 1),
            font_size=18  # Tăng kích thước font để nội dung spinner lớn hơn
        )
        self.hk_spinner.bind(text=self.select_hk)
        self.box.add_widget(self.hk_spinner)

        # Thêm ScrollView để chứa MDDataTable
        self.scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True
        )

        self.data_table = MDDataTable(
            size_hint=(1, None),
            height=dp(600),  # Chiều cao tối thiểu để bảng dài hơn
            use_pagination=False,
            elevation=0,
            column_data=[
                ("STT", dp(15)),
                ("Tên hoạt động", dp(90)),
                ("Cấp hoạt động", dp(35)),
                ("Loại hoạt động", dp(35)),
                ("GXN", dp(35)),
                ("Điểm", dp(35)),
            ],
            row_data=[]
        )
        self.scroll_view.add_widget(self.data_table)

        # Thêm label cho tổng điểm bên ngoài bảng, làm nổi bật
        self.total_label = MDLabel(
            text="Tổng điểm: 0",
            halign="right",
            size_hint=(1, None),
            height=dp(40),  # Tăng chiều cao để nổi bật
            font_size=20,  # Tăng kích thước font
            bold=True,  # In đậm
            theme_text_color="Custom",
            text_color=(0.17, 0.22, 0.49, 1)  # Màu xanh đậm để nổi bật, có thể thay đổi
        )
        self.box.add_widget(self.scroll_view)
        self.box.add_widget(self.total_label)

        root.add_widget(self.box)

        self.add_widget(root)
        self.load_hk_items()

    def back_to_main(self):
        self.manager.current = "student_main"

    def load_hk_items(self):
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
            rows = cur.fetchall()

        hk_items = [f"{name} ({year})" for id_hk, name, year in rows]
        self.hk_spinner.values = hk_items
        self.hk_ids = {f"{name} ({year})": id_hk for id_hk, name, year in rows}
        self.hk_spinner.text = "Vui lòng chọn học kỳ"

    def select_hk(self, spinner, text):
        if text == "Vui lòng chọn học kỳ":
            self.data_table.row_data = []
            self.total_label.text = "Tổng điểm: 0"
            self.debug_log.append("No semester selected")
            return
        self.selected_hk = text
        self.load_activities(text)

    def load_activities(self, hk_str):
        self.debug_log = []  # Xóa log cũ
        if not self.user or not hk_str:
            self.debug_log.append("No user or semester string provided")
            self.data_table.row_data = []
            self.total_label.text = "Tổng điểm: 0"
            return
        mssv = self.user["mssv"]
        id_hk = self.hk_ids.get(hk_str)

        if not id_hk:
            self.debug_log.append(f"No ID_HK found for {hk_str}")
            self.data_table.row_data = []
            self.total_label.text = "Tổng điểm: 0"
            return

        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
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
            self.debug_log.append(f"Found {len(activities)} activities for MSSV {mssv}, ID_HK {id_hk}")

            count_loai = {"Tình nguyện": False, "Hội nhập": False}
            max_cap = {"Chi hội": 2, "Liên chi": 3, "Trường": 2}
            count_cap = {"Chi hội": 0, "Liên chi": 0, "Trường": 0}
            used_gxn = False
            total = 0
            rows = []

            for i, (id_hd, ten, cap, loai, gxn) in enumerate(activities, 1):
                diem = 0
                if loai in count_loai and not count_loai[loai]:
                    diem += 4 if loai == "Tình nguyện" else 3
                    count_loai[loai] = True
                if cap in count_cap and count_cap[cap] < max_cap[cap]:
                    diem += 2 if cap == "Trường" else 1
                    count_cap[cap] += 1
                if str(gxn).strip().lower() == "có" and not used_gxn:
                    diem += 4
                    used_gxn = True

                total += diem
                display_ten = ten if len(ten) <= 20 else ten[:17] + "..."
                rows.append([str(i), display_ten, cap, loai, str(gxn), str(diem)])
                self.debug_log.append(f"Activity {i}: {ten}, Point: {diem}")

                cur.execute('''
                    UPDATE DIEM_DANH_HOAT_DONG
                    SET diem_cong=?
                    WHERE MSSV=? AND ID_HOAT_DONG=? AND ID_HK=?
                ''', (diem, mssv, id_hd, id_hk))

            self.debug_log.append(f"Total points: {total}")

            # Cập nhật tổng điểm vào bảng TONG_DIEM_HK
            cur.execute('''
                INSERT OR REPLACE INTO TONG_DIEM_HK (ID_SV, ID_HK, TONG_DIEM)
                VALUES (?, ?, ?)
            ''', (mssv, id_hk, total))
            conn.commit()

            if self.point_chart:
                self.point_chart.on_diem_danh_updated()

            # Xóa bảng cũ và tạo mới với dữ liệu cập nhật
            self.scroll_view.remove_widget(self.data_table)
            table_height = max(dp(50 * (len(rows) + 1)), dp(600))  # Giữ chiều cao lớn
            self.data_table = MDDataTable(
                size_hint=(1, None),
                height=table_height,
                use_pagination=False,
                elevation=0,
                column_data=[
                    ("STT", dp(15)),
                    ("Tên hoạt động", dp(90)),
                    ("Cấp hoạt động", dp(35)),
                    ("Loại hoạt động", dp(35)),
                    ("GXN", dp(35)),
                    ("Điểm", dp(35)),
                ],
                row_data=rows
            )
            self.scroll_view.add_widget(self.data_table)

            # Cập nhật label tổng điểm
            self.total_label.text = f"Tổng điểm: {total}"

            # Nếu có nhiều hoạt động, cuộn xuống dưới bảng
            def scroll_to_bottom(dt):
                self.scroll_view.scroll_y = 0
            Clock.schedule_once(scroll_to_bottom, 0.1)

    def get_debug_log(self):
        return "\n".join(self.debug_log)  # Trả về log để kiểm tra lỗi