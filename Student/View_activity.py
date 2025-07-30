import tkinter as tk
from tkinter import ttk
import sqlite3
from Student.Styles_student import BACK_BUTTON_STYLE, PAGE_BG_COLOR, TREEVIEW_STYLE, BUTTON_SEARCH_STYLE
from Database.Create_db import DB_NAME

def render_view_activity(container, user):
    all_data_rows = []
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg=PAGE_BG_COLOR)
    container.pack_propagate(False)

    def back_to_main():
        from Student.View_infor import render_view_infor
        render_view_infor(container, user)

    def load_hoat_dong(event=None):
        nonlocal all_data_rows
        for row in table.get_children():
            table.delete(row)

        all_data_rows.clear()

        hk_str = combo_hk.get()
        if not hk_str:
            return

        id_hk = int(hk_str.split(" - ")[0])
        mssv = user.get("mssv")

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TONG_DIEM_HK (
                    ID_SV TEXT,
                    ID_HK INTEGER,
                    TONG_DIEM INTEGER,
                    PRIMARY KEY (ID_SV, ID_HK)
                )
            ''')

            cursor.execute('''
                SELECT hd.ID_HD, hd.TEN_HD, hd.CAP_HD, hd.CATEGORY_HD, hd.CO_XAC_NHAN
                FROM DIEM_DANH_HOAT_DONG dd
                JOIN HOAT_DONG hd ON dd.id_hoat_dong = hd.ID_HD
                WHERE dd.MSSV = ? AND dd.id_hk = ?
            ''', (mssv, id_hk))
            data = cursor.fetchall()

            max_loai = {"Tình nguyện": 1, "Hội nhập": 1}
            max_cap = {"Chi hội": 2, "Liên chi": 3, "Trường": 2}

            count_loai = {"Tình nguyện": False, "Hội nhập": False}
            count_cap = {"Chi hội": 0, "Liên chi": 0, "Trường": 0}
            used_gxn = False

            tong_diem = 0

            for idx, row in enumerate(data, start=1):
                id_hd, ten_hd, cap_hd, loai_hd, co_xn = row
                diem = 0

                if loai_hd == "Tình nguyện" and not count_loai["Tình nguyện"]:
                    diem += 4
                    count_loai["Tình nguyện"] = True
                elif loai_hd == "Hội nhập" and not count_loai["Hội nhập"]:
                    diem += 3
                    count_loai["Hội nhập"] = True

                if cap_hd == "Chi hội" and count_cap["Chi hội"] < max_cap["Chi hội"]:
                    diem += 1
                    count_cap["Chi hội"] += 1
                elif cap_hd == "Liên chi" and count_cap["Liên chi"] < max_cap["Liên chi"]:
                    diem += 1
                    count_cap["Liên chi"] += 1
                elif cap_hd == "Trường" and count_cap["Trường"] < max_cap["Trường"]:
                    diem += 2
                    count_cap["Trường"] += 1

                if str(co_xn).strip().lower() == "có" and not used_gxn:
                    diem += 4
                    used_gxn = True

                tong_diem += diem

                table.insert("", "end", values=(idx, ten_hd, cap_hd, loai_hd, co_xn, diem))
                all_data_rows.append((idx, ten_hd, cap_hd, loai_hd, co_xn, diem))

                cursor.execute('''
                    UPDATE DIEM_DANH_HOAT_DONG
                    SET diem_cong = ?
                    WHERE MSSV = ? AND ID_HOAT_DONG = ? AND ID_HK = ?
                ''', (diem, mssv, id_hd, id_hk))

            cursor.execute('''
                INSERT INTO TONG_DIEM_HK (ID_SV, ID_HK, TONG_DIEM)
                VALUES (?, ?, ?)
                ON CONFLICT(ID_SV, ID_HK) DO UPDATE SET TONG_DIEM = excluded.TONG_DIEM
            ''', (mssv, id_hk, tong_diem))

        table.insert("", "end", values=("", "", "", "", "Tổng điểm học kỳ này:", tong_diem), tags=("summary",))
        style_rows()

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Student.Treeview",
                    background="white",
                    foreground="black",
                    rowheight=TREEVIEW_STYLE["rowheight"],
                    fieldbackground="white",
                    font=TREEVIEW_STYLE["font"])
    style.configure("Student.Treeview.Heading",
                    background=TREEVIEW_STYLE["header_bg"],
                    foreground=TREEVIEW_STYLE["header_fg"],
                    font=TREEVIEW_STYLE["header_font"])
    style.map("Student.Treeview.Heading", background=[], foreground=[])
    style.map("Student.Treeview",
              background=[('selected', '#e0e0e0')],
              foreground=[('selected', 'black')])
    style.layout("Student.Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    top_frame = tk.Frame(container, bg=PAGE_BG_COLOR)
    top_frame.pack(fill="x", pady=(10, 0))

    title_search_frame = tk.Frame(top_frame, bg=PAGE_BG_COLOR)
    title_search_frame.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(
        title_search_frame,
        text="✅ Hoạt động đã tham gia",
        font=TREEVIEW_STYLE["header_font"],
        fg="#00897B",
        bg=PAGE_BG_COLOR
    ).pack(side="left", padx=37)

    search_frame = tk.Frame(title_search_frame, bg=PAGE_BG_COLOR)
    search_frame.pack(side="right")

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 11), width=30)
    search_entry.pack(side="left", padx=(0, 5))

    def search_table():
        keyword = search_var.get().lower().strip()
        for row in table.get_children():
            table.delete(row)

        filtered = []
        for row in all_data_rows:
            if keyword in " ".join(str(val).lower() for val in row):
                filtered.append(row)

        for i, row in enumerate(filtered, start=1):
            table.insert("", "end", values=row)

        tong_diem = sum(int(row[-1]) for row in filtered) if filtered else 0
        table.insert("", "end", values=("", "", "", "", "Tổng điểm tìm được:", tong_diem), tags=("summary",))
        style_rows()

    search_button = tk.Button(search_frame, text="Tìm kiếm", command=search_table, **BUTTON_SEARCH_STYLE)
    search_button.pack(side="left")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
        hk_list = [f"{row[0]} - {row[1]} ({row[2]})" for row in cursor.fetchall()]

    hk_frame = tk.Frame(top_frame, bg=PAGE_BG_COLOR)
    hk_frame.pack(pady=(0, 10))

    tk.Label(hk_frame, text="Chọn học kỳ:", font=("Arial", 13, "bold"), bg=PAGE_BG_COLOR).pack(side="left", padx=5)
    combo_hk = ttk.Combobox(hk_frame, values=hk_list, font=("Arial", 11), state="readonly", width=30)
    combo_hk.pack(side="left", padx=5)
    combo_hk.bind("<<ComboboxSelected>>", load_hoat_dong)

    middle_frame = tk.Frame(container, bg=PAGE_BG_COLOR)
    middle_frame.pack(fill="both", expand=False, padx=20, pady=(0, 10))

    columns = ("STT", "Tên hoạt động", "Cấp", "Loại", "Giấy xác nhận", "Điểm")

    scrollbar = ttk.Scrollbar(middle_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    table = ttk.Treeview(
        middle_frame,
        columns=columns,
        show="headings",
        style="Student.Treeview",
        yscrollcommand=scrollbar.set
    )
    table.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=table.yview)

    for col, text, anchor, width in zip(columns,
                                        ["STT", "Tên hoạt động", "Cấp", "Loại", "Giấy xác nhận", "Điểm"],
                                        ["center", "w", "center", "center", "center", "center"],
                                        [40, 280, 130, 150, 150, 80]):
        table.heading(col, text=text)
        table.column(col, anchor=anchor, width=width)

    def block_resize_column(event):
        if table.identify_region(event.x, event.y) == "separator":
            return "break"

    table.bind("<Button-1>", block_resize_column)
    table.bind("<B1-Motion>", block_resize_column)

    def on_treeview_select(event):
        selected = table.selection()
        for item in selected:
            if "summary" in table.item(item, "tags"):
                table.selection_remove(item)

    table.bind("<<TreeviewSelect>>", on_treeview_select)

    def style_rows():
        for i, item in enumerate(table.get_children()):
            if "summary" in table.item(item, "tags"):
                table.item(item, tags=("summary",))
            else:
                table.item(item, tags=("even",) if i % 2 == 0 else ("odd",))
        table.tag_configure("even", background=TREEVIEW_STYLE["even_row_bg"])
        table.tag_configure("odd", background=TREEVIEW_STYLE["odd_row_bg"])
        table.tag_configure("summary",
                            background=TREEVIEW_STYLE["header_bg"],
                            foreground=TREEVIEW_STYLE["header_fg"],
                            font=TREEVIEW_STYLE["header_font"])

    bottom_frame = tk.Frame(container, bg=PAGE_BG_COLOR)
    bottom_frame.pack(side="bottom", fill="x", padx=20, pady=10)

    btn_back = tk.Button(
        bottom_frame,
        text="← Quay lại",
        width=9,
        height=1,
        font=BACK_BUTTON_STYLE.get("font"),
        command=back_to_main,
        bg=BACK_BUTTON_STYLE.get("bg"),
        fg=BACK_BUTTON_STYLE.get("fg"),
        activebackground=BACK_BUTTON_STYLE.get("activebackground")
    )
    btn_back.pack(side="left", padx=10, pady=10)
