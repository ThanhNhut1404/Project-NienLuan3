import tkinter as tk
from tkinter import ttk
import sqlite3
from Student.Styles_student import BACK_BUTTON_STYLE, PAGE_BG_COLOR, TREEVIEW_STYLE
from Database.Create_db import DB_NAME

def render_view_activity(container, user):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg=PAGE_BG_COLOR)
    container.pack_propagate(False)  # Không cho pack tự co

    def back_to_main():
        from Student.View_infor import render_view_infor
        render_view_infor(container, user)

    def load_hoat_dong(event=None):
        for row in table.get_children():
            table.delete(row)

        hk_str = combo_hk.get()
        if not hk_str:
            return

        id_hk = int(hk_str.split(" - ")[0])
        mssv = user.get("mssv")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT hd.TEN_HD, hd.CAP_HD, hd.CATEGORY_HD, hd.CO_XAC_NHAN
            FROM DIEM_DANH_HOAT_DONG dd
            JOIN HOAT_DONG hd ON dd.id_hoat_dong = hd.ID_HD
            WHERE dd.MSSV = ? AND dd.id_hk = ?
        ''', (mssv, id_hk))
        data = cursor.fetchall()
        conn.close()

        for idx, row in enumerate(data, start=1):
            table.insert("", "end", values=(idx, *row))
        style_rows()

    # ====== STYLE TREEVIEW ======
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

    # ====== TOP FRAME ======
    top_frame = tk.Frame(container, bg=PAGE_BG_COLOR)
    top_frame.pack(fill="x", pady=(10, 0))

    tk.Label(
        top_frame,
        text="✅ Hoạt động đã tham gia",
        font=TREEVIEW_STYLE["header_font"],
        fg="#00897B",
        bg=PAGE_BG_COLOR
    ).pack(anchor="w", padx=70, pady=(0, 10))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
    hk_list = [f"{row[0]} - {row[1]} ({row[2]})" for row in cursor.fetchall()]
    conn.close()

    hk_frame = tk.Frame(top_frame, bg=PAGE_BG_COLOR)
    hk_frame.pack(pady=(0, 10))

    tk.Label(hk_frame, text="Chọn học kỳ:", font=("Arial", 13, "bold"), bg=PAGE_BG_COLOR).pack(side="left", padx=5)
    combo_hk = ttk.Combobox(hk_frame, values=hk_list, font=("Arial", 11), state="readonly", width=30)
    combo_hk.pack(side="left", padx=5)
    combo_hk.bind("<<ComboboxSelected>>", load_hoat_dong)

    # ====== MIDDLE FRAME (TABLE) ======
    middle_frame = tk.Frame(container, bg=PAGE_BG_COLOR)
    middle_frame.pack(fill="both", expand=False, padx=20, pady=(0, 10))

    columns = ("STT", "Tên hoạt động", "Cấp", "Loại", "Giấy xác nhận")
    table = ttk.Treeview(middle_frame, columns=columns, show="headings", style="Student.Treeview")
    table.config(height=14)
    table.pack(side="left", fill="both", expand=True)

    table.heading("STT", text="STT")
    table.column("STT", anchor="center", width=40)

    table.heading("Tên hoạt động", text="Tên hoạt động")
    table.column("Tên hoạt động", anchor="w", width=280)

    table.heading("Cấp", text="Cấp")
    table.column("Cấp", anchor="center", width=130)

    table.heading("Loại", text="Loại")
    table.column("Loại", anchor="center", width=150)

    table.heading("Giấy xác nhận", text="Giấy xác nhận")
    table.column("Giấy xác nhận", anchor="center", width=150)

    def block_resize_column(event):
        if table.identify_region(event.x, event.y) == "separator":
            return "break"
    table.bind("<Button-1>", block_resize_column)
    table.bind("<B1-Motion>", block_resize_column)

    def style_rows():
        for i, item in enumerate(table.get_children()):
            table.item(item, tags=("even",) if i % 2 == 0 else ("odd",))
        table.tag_configure("even", background=TREEVIEW_STYLE["even_row_bg"])
        table.tag_configure("odd", background=TREEVIEW_STYLE["odd_row_bg"])

    # ====== BOTTOM FRAME (BUTTON LUÔN DƯỚI) ======
    bottom_frame = tk.Frame(container, bg=PAGE_BG_COLOR)
    bottom_frame.pack(side="bottom", fill="x", padx=20, pady=10)

    btn_back = tk.Button(
        bottom_frame,
        text="← Quay lại",
        width=9,
        height=1,
        command=back_to_main,
        **BACK_BUTTON_STYLE
    )
    btn_back.pack(side="left", padx=10, pady=10)
