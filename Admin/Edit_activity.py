import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from copy import deepcopy
from Admin.Styles_admin import *

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

        return diem_cap + diem_loai + diem_xn

    def on_back():
        if go_back:
            go_back()

    for widget in container.winfo_children():
        widget.destroy()
    container.configure(bg="white")

    cursor.execute("SELECT * FROM HOAT_DONG WHERE ID_HD = ?", (id_hd,))
    data = cursor.fetchone()
    if not data:
        messagebox.showerror("Lỗi", "Không tìm thấy hoạt động.")
        return

    ten_hd, loai_hd, cap_hd, gio_bd, gio_kt, diem_cong, co_xac_nhan, ngay_tc, id_hk = data[1:10]

    print("Xác nhận")
    print("Giờ bắt đầu:", gio_bd)
    print("Giờ kết thúc:", gio_kt)

    cursor.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
    ds_hk = cursor.fetchall()
    hk_list = [f"{row[0]} - {row[1]} {row[2]}" for row in ds_hk]
    hk_map = {f"{row[0]} - {row[1]} {row[2]}": row[0] for row in ds_hk}

    def update_hoat_dong():
        try:
            ten = entry_ten.get().strip()
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

    # Đặt màu nền cho toàn bộ giao diện
    container.config(bg=PAGE_BG_COLOR)

    # Tiêu đề trên cùng
    tk.Label(
        container,
        text="🛠️ Sửa hoạt động",
        font=TITLE_FONT,
        bg="white",
        fg="#003366"
    ).pack(anchor="w", padx=28, pady=(20, 5))

    # Khung ô vuông màu xanh chứa form
    outer_frame = tk.Frame(
        container,
        bg=FORM_BG_COLOR,
        bd=FORM_BORDER_WIDTH,
        relief=FORM_BORDER_STYLE,
        width=480
    )
    outer_frame.pack(pady=10)

    # === Form trong khung viền màu xanh ===
    form_frame = tk.Frame(outer_frame, bg=FORM_BG_COLOR)
    form_frame.pack(padx=FORM_PADDING_X, pady=FORM_PADDING_Y)

    form_inner = tk.Frame(form_frame, bg=FORM_BG_COLOR)
    form_inner.pack()

    # === Ô nhập liệu ===
    tk.Label(form_inner, text="Tên hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR,
             fg="white").grid(row=0, column=0, pady=6)
    entry_ten = tk.Entry(form_inner, **ENTRY_STYLE_ACTIVITY)
    entry_ten.grid(row=0, column=1, pady=6)
    entry_ten.insert(0, ten_hd)

    tk.Label(form_inner, text="Loại hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR,
             fg="white").grid(row=1, column=0, pady=6)
    combo_loai = ttk.Combobox(form_inner, font=("Arial", 10), width=29, state="readonly",
                              values=["Tình nguyện", "Hội nhập", "Khác"])
    combo_loai.grid(row=1, column=1, pady=6)
    combo_loai.set(loai_hd if loai_hd in combo_loai['values'] else "Khác")

    tk.Label(form_inner, text="Cấp hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR,
             fg="white").grid(row=2, column=0, pady=6)
    combo_cap = ttk.Combobox(form_inner, font=("Arial", 10), width=29, state="readonly",
                             values=["Chi hội", "Liên chi", "Trường"])
    combo_cap.grid(row=2, column=1, pady=6)
    combo_cap.set(cap_hd if cap_hd in combo_cap['values'] else "Trường")

    tk.Label(form_inner, text="Có giấy xác nhận:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR,
             fg="white").grid(row=3, column=0, pady=6)
    xn_var = tk.StringVar(value=co_xac_nhan if co_xac_nhan in ["Có", "Không"] else "Không")
    xn_frame = tk.Frame(form_inner, bg=FORM_BG_COLOR)
    xn_frame.grid(row=3, column=1, padx=FORM_ENTRY_PADX, pady=6, sticky="w")
    for text in ["Có", "Không"]:
        tk.Radiobutton(
            xn_frame,
            text=text,
            variable=xn_var,
            value=text,
            bg=FORM_BG_COLOR,
            fg="white",
            font=ENTRY_FONT,
            selectcolor="black",
            activebackground=FORM_BG_COLOR,
            activeforeground="white",
        ).pack(side="left", padx=(0, 10))

    tk.Label(form_inner, text="Ngày tổ chức:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR,
             fg="white").grid(row=4, column=0, pady=6)
    calendar_ngay = DateEntry(form_inner, **DATE_ENTRY_STYLE)
    calendar_ngay.grid(row=4, column=1, pady=6)
    try:
        calendar_ngay.set_date(datetime.strptime(ngay_tc, "%d/%m/%Y").date())
    except:
        pass

    tk.Label(form_inner, text="Giờ bắt đầu:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(
        row=5, column=0, pady=6)
    start_time_frame = tk.Frame(form_inner, bg=FORM_BG_COLOR)
    start_time_frame.grid(row=5, column=1, pady=6, sticky="w")
    start_hour_style = deepcopy(SPINBOX_STYLE)
    start_hour_style["to"] = 23
    spin_start_hour = tk.Spinbox(start_time_frame, **start_hour_style)
    spin_start_hour.pack(side="left")
    tk.Label(start_time_frame, text="giờ", bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT).pack(side="left",
                                                                                               padx=(5, 15))
    spin_start_min = tk.Spinbox(start_time_frame, **SPINBOX_STYLE)
    spin_start_min.pack(side="left")
    tk.Label(start_time_frame, text="phút", bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT).pack(side="left",
                                                                                                padx=(5, 0))
    try:
        h, m, *_ = map(int, gio_bd.strip().split(":"))
        spin_start_hour.delete(0, 'end')
        spin_start_min.delete(0, 'end')
        spin_start_hour.insert(0, f"{h:02}")
        spin_start_min.insert(0, f"{m:02}")
    except:
        pass

    tk.Label(form_inner, text="Giờ kết thúc:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR,
             fg="white").grid(row=6, column=0, pady=6)
    end_time_frame = tk.Frame(form_inner, bg=FORM_BG_COLOR)
    end_time_frame.grid(row=6, column=1, pady=6, sticky="w")
    end_hour_style = deepcopy(SPINBOX_STYLE)
    end_hour_style["to"] = 23
    spin_end_hour = tk.Spinbox(end_time_frame, **end_hour_style)
    spin_end_hour.pack(side="left")
    tk.Label(end_time_frame, text="giờ", bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT).pack(side="left", padx=(5, 15))
    spin_end_min = tk.Spinbox(end_time_frame, **SPINBOX_STYLE)
    spin_end_min.pack(side="left")
    tk.Label(end_time_frame, text="phút", bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT).pack(side="left", padx=(5, 0))
    try:
        h, m, *_ = map(int, gio_kt.strip().split(":"))
        spin_end_hour.delete(0, 'end')
        spin_end_min.delete(0, 'end')
        spin_end_hour.insert(0, f"{h:02}")
        spin_end_min.insert(0, f"{m:02}")
    except:
        pass

    tk.Label(form_inner, text="Học kỳ - Năm học:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR,
             fg="white").grid(row=7, column=0, pady=6)
    combo_hk = ttk.Combobox(form_inner, font=("Arial", 10), width=29, state="readonly", values=hk_list)
    combo_hk.grid(row=7, column=1, pady=6)
    for hk_str in hk_list:
        if hk_str.startswith(f"{id_hk} -"):
            combo_hk.set(hk_str)
            break

    # === Nút chức năng trong ô vuông ===
    button_frame = tk.Frame(form_inner, bg=FORM_BG_COLOR)
    button_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0), sticky="ew")
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    btn_back = tk.Button(
        button_frame,
        text="← Quay lại",
        command=on_back,
        **BACK_BUTTON_STYLE
    )
    btn_back.grid(row=0, column=0, sticky="w", padx=10)

    btn_save = tk.Button(
        button_frame,
        text="Lưu thay đổi",
        command=update_hoat_dong,
        **CREATE_BUTTON_STYLE
    )
    btn_save.grid(row=0, column=1, sticky="e", padx=10)

