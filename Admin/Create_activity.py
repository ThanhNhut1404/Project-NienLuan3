import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
import os
import qrcode
from Admin.Styles_admin import *
from datetime import datetime
from Database.Create_db import DB_NAME
from copy import deepcopy
from Admin.Admin_main import render_admin_main

QR_FOLDER = "QR_HOAT_DONG"
os.makedirs(QR_FOLDER, exist_ok=True)

def tao_qr_hoat_dong(id_hd, ten_hd):
    qr_data = f"HOATDONG:{id_hd}"
    qr_img = qrcode.make(qr_data)
    filename = f"QR_HD{id_hd}_{ten_hd.replace(' ', '_')}.png"
    filepath = os.path.join(QR_FOLDER, filename)
    qr_img.save(filepath)
    return filepath

def render_Create_activity(container):
    for widget in container.winfo_children():
        widget.destroy()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
    hk_data = cursor.fetchall()
    hk_map = {f"{row[1]} ({row[2]})": row[0] for row in hk_data}  # key hiển thị, value là ID_HK
    hk_list = list(hk_map.keys())

    def tinh_diem():
        cap = combo_cap.get()
        loai = combo_loai.get()
        xn = xn_var.get()

        diem_cap = 2 if cap == "Trường" else 1 if cap in ["Chi hội", "Liên chi"] else 0
        diem_loai = 4 if loai == "Tình nguyện" else 3 if loai == "Hội nhập" else 0
        diem_xn = 4 if xn == "Có" else 0

        tong = diem_cap + diem_loai + diem_xn
        diem_label.config(text=f"➞ Tổng điểm cộng: {tong}")
        return tong

    def clear_form():
        entry_dia_chi.delete(0, tk.END)
        entry_ten.delete(0, tk.END)
        combo_loai.set("")
        combo_cap.set("")
        combo_hk.set("")
        xn_var.set("Không")
        diem_label.config(text="➞ Tổng điểm cộng: 0")

    def tao_hoat_dong():
        ten_hd = entry_ten.get().strip()
        loai_hd = combo_loai.get().strip()
        cap_hd = combo_cap.get().strip()
        ngay_to_chuc = calendar_ngay.get_date().strftime("%d/%m/%Y")
        gio_bd = f"{spin_start_hour.get()}:{spin_start_min.get()}:00"
        gio_kt = f"{spin_end_hour.get()}:{spin_end_min.get()}:00"
        co_xn = xn_var.get()
        hk_str = combo_hk.get().strip()
        dia_chi = entry_dia_chi.get().strip()

        if not ten_hd:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên hoạt động.")
            return
        if not hk_str:
            messagebox.showwarning("Thiếu học kỳ", "Vui lòng chọn học kỳ – năm học.")
            return

        id_hk = hk_map.get(hk_str)
        if id_hk is None:
            messagebox.showerror("Lỗi", "Không xác định được học kỳ.")
            return

        diem_cong = tinh_diem()

        if id_hk is None:
            messagebox.showerror("Lỗi", "Không xác định được học kỳ.")
            return

        try:
            cursor.execute('''
                INSERT INTO HOAT_DONG (TEN_HD, CATEGORY_HD, CAP_HD, START_TIME, TIME_OUT, NGAY_TO_CHUC, DIA_CHI_HD, DIEM_CONG, CO_XAC_NHAN, ID_HK)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ten_hd, loai_hd, cap_hd, gio_bd, gio_kt, ngay_to_chuc, dia_chi, diem_cong, co_xn, id_hk))

            conn.commit()

            id_hd = cursor.lastrowid
            qr_path = tao_qr_hoat_dong(id_hd, ten_hd)

            clear_form()
            from Admin.View_qr_imge import show_qr_image
            show_qr_image(container, qr_path)

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def back_to_main():
        from Admin.Admin_main import render_admin_main
        render_admin_main(container.master)

    container.config(bg=PAGE_BG_COLOR)
    tk.Label(
        container,
        text="📅 Tạo hoạt động",
        font=TITLE_FONT,
        bg="white",
        fg="#003366"
    ).pack(anchor="w", padx=28, pady=(20, 5))

    outer_frame = tk.Frame(
        container,
        bg=FORM_BG_COLOR,
        bd=FORM_BORDER_WIDTH,
        relief=FORM_BORDER_STYLE,
        width=480
    )
    outer_frame.pack(pady=10)

    form_frame = tk.Frame(outer_frame, bg=FORM_BG_COLOR)
    form_frame.pack(padx=FORM_PADDING_X, pady=FORM_PADDING_Y)

    form_inner = tk.Frame(form_frame, bg=FORM_BG_COLOR)
    form_inner.pack()

    tk.Label(form_inner, text="Tên hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=0, column=0, pady=6)
    entry_ten = tk.Entry(form_inner, **ENTRY_STYLE_ACTIVITY)
    entry_ten.grid(row=0, column=1, pady=6)

    tk.Label(form_inner, text="Loại hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=1, column=0, pady=6)
    combo_loai = ttk.Combobox(form_inner, font=("Arial", 10), width=29, state="readonly")
    combo_loai['values'] = ["Tình nguyện", "Hội nhập", "Khác"]
    combo_loai.grid(row=1, column=1, pady=6)
    combo_loai.bind("<<ComboboxSelected>>", lambda e: tinh_diem())

    tk.Label(form_inner, text="Cấp hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=2, column=0, pady=6)
    combo_cap = ttk.Combobox(form_inner, font=("Arial", 10), width=29, state="readonly")
    combo_cap['values'] = ["Chi hội", "Liên chi", "Trường"]
    combo_cap.grid(row=2, column=1, pady=6)
    combo_cap.bind("<<ComboboxSelected>>", lambda e: tinh_diem())

    tk.Label(form_inner, text="Có giấy xác nhận:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=3, column=0, pady=6)
    xn_var = tk.StringVar(value="Không")
    xn_frame = tk.Frame(form_inner, bg=FORM_BG_COLOR)
    xn_frame.grid(row=3, column=1, padx=FORM_ENTRY_PADX, pady=6, sticky="w")

    for text in ["Có", "Không"]:
        tk.Radiobutton(
            xn_frame,
            text=text,
            variable=xn_var,
            value=text,
            command=tinh_diem,
            bg=FORM_BG_COLOR,
            fg="white",
            font=ENTRY_FONT,
            selectcolor="black",
            activebackground=FORM_BG_COLOR,
            activeforeground="white",
        ).pack(side="left", padx=(0, 10))

    tk.Label(form_inner, text="Ngày tổ chức:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=4, column=0, pady=6)
    calendar_ngay = DateEntry(form_inner, **DATE_ENTRY_STYLE)
    calendar_ngay.grid(row=4, column=1, pady=6)

    tk.Label(form_inner, text="Địa chỉ:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR,
             fg="white").grid(row=5, column=0, pady=6)
    entry_dia_chi = tk.Entry(form_inner, **ENTRY_STYLE_ACTIVITY)
    entry_dia_chi.grid(row=5, column=1, pady=6)

    tk.Label(form_inner, text="Bắt đầu:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=6, column=0, pady=6)
    start_time_frame = tk.Frame(form_inner, bg=FORM_BG_COLOR)
    start_time_frame.grid(row=6, column=1, pady=6, sticky="w")

    start_hour_style = deepcopy(SPINBOX_STYLE)
    start_hour_style["to"] = 23
    spin_start_hour = tk.Spinbox(start_time_frame, **start_hour_style)
    spin_start_hour.pack(side="left")
    tk.Label(start_time_frame, text="giờ", bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT).pack(side="left", padx=(5, 15))
    spin_start_min = tk.Spinbox(start_time_frame, **SPINBOX_STYLE)
    spin_start_min.pack(side="left")
    tk.Label(start_time_frame, text="phút", bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT).pack(side="left", padx=(5, 0))

    tk.Label(form_inner, text="Kết thúc:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=7, column=0, pady=6)
    end_time_frame = tk.Frame(form_inner, bg=FORM_BG_COLOR)
    end_time_frame.grid(row=7, column=1, pady=6, sticky="w")

    end_hour_style = deepcopy(SPINBOX_STYLE)
    end_hour_style["to"] = 23
    spin_end_hour = tk.Spinbox(end_time_frame, **end_hour_style)
    spin_end_hour.pack(side="left")
    tk.Label(end_time_frame, text="giờ", bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT).pack(side="left", padx=(5, 15))
    spin_end_min = tk.Spinbox(end_time_frame, **SPINBOX_STYLE)
    spin_end_min.pack(side="left")
    tk.Label(end_time_frame, text="phút", bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT).pack(side="left", padx=(5, 0))

    tk.Label(form_inner, text="Học kỳ - Năm học:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=9, column=0, pady=6)
    combo_hk = ttk.Combobox(form_inner, font=("Arial", 10), width=29, state="readonly", values=hk_list)
    combo_hk.grid(row=9, column=1, pady=6)

    diem_label = tk.Label(
        form_inner,
        text="➞ Tổng điểm cộng: 0",
        font=("Arial", 13, "bold"),
        fg="red",
        bg=FORM_BG_COLOR,
        anchor="center"
    )
    diem_label.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(10, 5))

    btn_create = tk.Button(
        form_inner,
        text="Tạo hoạt động",
        command=tao_hoat_dong,
        **CREATE_BUTTON_STYLE
    )
    btn_create.grid(row=12, column=1, pady=(20, 10), sticky="e")

    btn_back = tk.Button(
        form_inner,
        text="← Quay lại",
        command=back_to_main,
        **BACK_BUTTON_STYLE
    )
    btn_back.grid(row=12, column=0, pady=(20, 10), sticky="w")
