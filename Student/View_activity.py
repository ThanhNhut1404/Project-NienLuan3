import tkinter as tk
from tkinter import ttk
import sqlite3
from Database.Create_db import DB_NAME

def render_view_activity(container, user):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg="white")

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
            ten_hd, cap, loai, xn = row
            table.insert("", "end", values=(idx, ten_hd, cap, loai, xn))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
    hk_list = [f"{row[0]} - {row[1]} ({row[2]})" for row in cursor.fetchall()]
    conn.close()

    tk.Label(container, text="📅 HOẠT ĐỘNG ĐÃ THAM GIA", font=("Arial", 16, "bold"), fg="#003366", bg="white").pack(pady=10)

    hk_frame = tk.Frame(container, bg="white")
    hk_frame.pack(pady=5)

    tk.Label(hk_frame, text="Chọn học kỳ:", font=("Arial", 11), bg="white").pack(side="left", padx=5)
    combo_hk = ttk.Combobox(hk_frame, values=hk_list, font=("Arial", 11), state="readonly", width=30)
    combo_hk.pack(side="left", padx=5)
    combo_hk.bind("<<ComboboxSelected>>", load_hoat_dong)

    table_frame = tk.Frame(container)
    table_frame.pack(padx=20, pady=10, fill="both", expand=True)

    columns = ("STT", "Tên hoạt động", "Cấp", "Loại", "Giấy xác nhận")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center")
    table.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tk.Button(container, text="⬅️ Quay lại", font=("Arial", 11), bg="#cccccc", command=back_to_main).pack(pady=10)
