import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

from Database.Create_db import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

def render_edit_activity(container, id_hd, go_back):
    def tinh_diem():
        cap = combo_cap.get()
        loai = combo_loai.get()
        xn = xn_var.get()

        diem_cap = 2 if cap == "Trường" else 1 if cap in ["Chi hội", "Liên chi"] else 0
        diem_loai = 4 if loai == "Tình nguyện" else 3 if loai == "Hội nhập" else 0
        diem_xn = 4 if xn == "Có" else 0

        tong = diem_cap + diem_loai + diem_xn
        return tong

    def on_back():
        if go_back:
            go_back()

    for widget in container.winfo_children():
        widget.destroy()
    container.configure(bg="white")

    # LẤY DỮ LIỆU HOẠT ĐỘNG
    cursor.execute("SELECT * FROM HOAT_DONG WHERE ID_HD = ?", (id_hd,))
    data = cursor.fetchone()
    if not data:
        messagebox.showerror("Lỗi", "Không tìm thấy hoạt động.")
        return

    ten_hd, loai_hd, cap_hd, co_xac_nhan, ngay_tc, gio_bd, gio_kt, diem_cong, id_hk = data[1:10]

    # LẤY DANH SÁCH HỌC KỲ
    cursor.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
    ds_hk = cursor.fetchall()
    hk_list = [f"{row[0]} - {row[1]} {row[2]}" for row in ds_hk]
    hk_map = {f"{row[0]} - {row[1]} {row[2]}": row[0] for row in ds_hk}

    # GIAO DIỆN
    tk.Label(container, text="✏️ Sửa hoạt động", font=("Arial", 16, "bold"), fg="#003366", bg="white").pack(pady=10)
    form = tk.Frame(container, bg="#f9f9f9", padx=20, pady=20)
    form.pack()

    tk.Label(form, text="Tên hoạt động:", font=("Arial", 10), width=18, anchor="e", bg="#f9f9f9").grid(row=0, column=0, pady=6)
    entry_ten = tk.Entry(form, font=("Arial", 10), width=35)
    entry_ten.grid(row=0, column=1, pady=6)
    entry_ten.insert(0, ten_hd)

    tk.Label(form, text="Loại hoạt động:", font=("Arial", 10), width=18, anchor="e", bg="#f9f9f9").grid(row=1, column=0, pady=6)
    combo_loai = ttk.Combobox(form, font=("Arial", 10), width=33, state="readonly",
                              values=["Tình nguyện", "Hội nhập", "Khác"])
    combo_loai.grid(row=1, column=1, pady=6)
    combo_loai.set(loai_hd if loai_hd in combo_loai['values'] else "Khác")

    tk.Label(form, text="Cấp hoạt động:", font=("Arial", 10), width=18, anchor="e", bg="#f9f9f9").grid(row=2, column=0, pady=6)
    combo_cap = ttk.Combobox(form, font=("Arial", 10), width=33, state="readonly",
                             values=["Chi hội", "Liên chi", "Trường"])
    combo_cap.grid(row=2, column=1, pady=6)
    combo_cap.set(cap_hd if cap_hd in combo_cap['values'] else "Trường")

    tk.Label(form, text="Có giấy xác nhận:", font=("Arial", 10), width=18, anchor="e", bg="#f9f9f9").grid(row=3, column=0, pady=6)
    xn_var = tk.StringVar(value=co_xac_nhan or "Không")
    tk.Radiobutton(form, text="Có", variable=xn_var, value="Có", bg="#f9f9f9").grid(row=3, column=1, sticky="w")
    tk.Radiobutton(form, text="Không", variable=xn_var, value="Không", bg="#f9f9f9").grid(row=3, column=1, sticky="e")

    tk.Label(form, text="Ngày tổ chức:", font=("Arial", 10), width=18, anchor="e", bg="#f9f9f9").grid(row=4, column=0, pady=6)
    calendar_ngay = DateEntry(form, width=32, date_pattern='dd/mm/yyyy', background='darkblue', foreground='white')
    calendar_ngay.grid(row=4, column=1, pady=6)
    try:
        calendar_ngay.set_date(datetime.strptime(ngay_tc, "%d/%m/%Y"))
    except:
        pass

    tk.Label(form, text="Giờ bắt đầu (HH:mm):", font=("Arial", 10), width=18, anchor="e", bg="#f9f9f9").grid(row=5, column=0, pady=6)
    spin_start_hour = tk.Spinbox(form, from_=0, to=23, width=5, format="%02.0f")
    spin_start_min = tk.Spinbox(form, from_=0, to=59, width=5, format="%02.0f")
    spin_start_hour.grid(row=5, column=1, sticky="w", padx=(0, 50))
    spin_start_min.grid(row=5, column=1, sticky="e")
    try:
        h, m, *_ = map(int, gio_bd.split(":"))
        spin_start_hour.delete(0, 'end')
        spin_start_min.delete(0, 'end')
        spin_start_hour.insert(0, f"{h:02}")
        spin_start_min.insert(0, f"{m:02}")
    except:
        pass

    tk.Label(form, text="Giờ kết thúc (HH:mm):", font=("Arial", 10), width=18, anchor="e", bg="#f9f9f9").grid(row=6, column=0, pady=6)
    spin_end_hour = tk.Spinbox(form, from_=0, to=23, width=5, format="%02.0f")
    spin_end_min = tk.Spinbox(form, from_=0, to=59, width=5, format="%02.0f")
    spin_end_hour.grid(row=6, column=1, sticky="w", padx=(0, 50))
    spin_end_min.grid(row=6, column=1, sticky="e")
    try:
        h, m, *_ = map(int, gio_kt.split(":"))
        spin_end_hour.delete(0, 'end')
        spin_end_min.delete(0, 'end')
        spin_end_hour.insert(0, f"{h:02}")
        spin_end_min.insert(0, f"{m:02}")
    except:
        pass

    tk.Label(form, text="Học kỳ - Năm học:", font=("Arial", 10), width=18, anchor="e", bg="#f9f9f9").grid(row=7, column=0, pady=6)
    combo_hk = ttk.Combobox(form, font=("Arial", 10), width=33, state="readonly", values=hk_list)
    combo_hk.grid(row=7, column=1, pady=6)
    for hk_str in hk_list:
        if hk_str.startswith(f"{id_hk} -"):
            combo_hk.set(hk_str)
            break

    def update_hoat_dong():
        try:
            ten = entry_ten.get()
            loai = combo_loai.get()
            cap = combo_cap.get()
            xn = xn_var.get()
            ngay = calendar_ngay.get_date().strftime("%d/%m/%Y")
            gio_bd = f"{int(spin_start_hour.get()):02}:{int(spin_start_min.get()):02}:00"
            gio_kt = f"{int(spin_end_hour.get()):02}:{int(spin_end_min.get()):02}:00"
            hk_text = combo_hk.get()
            id_hk_value = hk_map.get(hk_text)

            if not id_hk_value:
                messagebox.showerror("Lỗi", "Vui lòng chọn học kỳ hợp lệ.")
                return

            diem_cong = tinh_diem()

            cursor.execute("""
                UPDATE HOAT_DONG
                SET TEN_HD = ?, CATEGORY_HD = ?, CAP_HD = ?, START_TIME = ?, TIME_OUT = ?, 
                    DIEM_CONG = ?, CO_XAC_NHAN = ?, NGAY_TO_CHUC = ?, ID_HK = ?
                WHERE ID_HD = ?
            """, (ten, loai, cap, gio_bd, gio_kt, diem_cong, xn, ngay, id_hk_value, id_hd))

            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật hoạt động thành công!")
            on_back()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Cập nhật thất bại: {e}")

    tk.Button(container, text="📂 Lưu thay đổi", bg="#006699", fg="white",
              font=("Arial", 11, "bold"), command=update_hoat_dong).pack(pady=10)

    tk.Button(container, text="↩ Quay lại", bg="gray", fg="white",
              font=("Arial", 10), command=on_back).pack(pady=5)