import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
import os
import qrcode
from Admin.Styles_admin import *
from datetime import datetime
from Database.Create_db import DB_NAME


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

    # ================== KẾT NỐI DB VÀ LẤY HỌC KỲ ===================
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT ID_HK, NAME_HK, SCHOOL_YEAR FROM HK_NK")
    hk_data = cursor.fetchall()
    hk_list = [f"{row[0]} - {row[1]} ({row[2]})" for row in hk_data]

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

        if not ten_hd:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên hoạt động.")
            return
        if not hk_str:
            messagebox.showwarning("Thiếu học kỳ", "Vui lòng chọn học kỳ – năm học.")
            return

        diem_cong = tinh_diem()
        id_hk = int(hk_str.split(" - ")[0])

        try:
            cursor.execute('''
                INSERT INTO HOAT_DONG (TEN_HD, CATEGORY_HD, CAP_HD, START_TIME, TIME_OUT, NGAY_TO_CHUC, DIEM_CONG, CO_XAC_NHAN, ID_HK)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ten_hd, loai_hd, cap_hd, gio_bd, gio_kt, ngay_to_chuc, diem_cong, co_xn, id_hk))
            conn.commit()

            id_hd = cursor.lastrowid
            qr_path = tao_qr_hoat_dong(id_hd, ten_hd)

            clear_form()
            from Admin.View_qr_imge import show_qr_image
            show_qr_image(container, qr_path)

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ========== GIAO DIỆN ==========
    container.config(bg=PAGE_BG_COLOR)
    tk.Label(
        container,
        text="📝 Tạo hoạt động",
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

    # Tên hoạt động
    tk.Label(form_frame, text="Tên hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=0, column=0, pady=6)
    entry_ten = tk.Entry(form_frame, **ENTRY_STYLE_ACTIVITY)
    entry_ten.grid(row=0, column=1, pady=6)

    # Loại hoạt động
    tk.Label(form_frame, text="Loại hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=1, column=0, pady=6)
    combo_loai = ttk.Combobox(form_frame, font=("Arial", 10), width=33, state="readonly")
    combo_loai['values'] = ["Tình nguyện", "Hội nhập", "Khác"]
    combo_loai.grid(row=1, column=1, pady=6)
    combo_loai.bind("<<ComboboxSelected>>", lambda e: tinh_diem())

    # Cấp hoạt động
    tk.Label(form_frame, text="Cấp hoạt động:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=2, column=0, pady=6)
    combo_cap = ttk.Combobox(form_frame, font=("Arial", 10), width=33, state="readonly")
    combo_cap['values'] = ["Chi hội", "Liên chi", "Trường"]
    combo_cap.grid(row=2, column=1, pady=6)
    combo_cap.bind("<<ComboboxSelected>>", lambda e: tinh_diem())

    # Giấy xác nhận
    tk.Label(form_frame, text="Có giấy xác nhận:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=3, column=0, pady=6)
    xn_var = tk.StringVar(value="Không")
    tk.Radiobutton(form_frame, text="Có", variable=xn_var, value="Có", command=tinh_diem, bg=FORM_BG_COLOR).grid(row=3, column=1, sticky="w")
    tk.Radiobutton(form_frame, text="Không", variable=xn_var, value="Không", command=tinh_diem, bg=FORM_BG_COLOR).grid(row=3, column=1, sticky="e")

    # Ngày tổ chức
    tk.Label(form_frame, text="Ngày tổ chức:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=4, column=0, pady=6)
    calendar_ngay = DateEntry(form_frame, width=32, date_pattern='dd/mm/yyyy', background='darkblue', foreground='white')
    calendar_ngay.grid(row=4, column=1, pady=6)

    # Giờ bắt đầu
    tk.Label(form_frame, text="Giờ bắt đầu (HH:mm):", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=5, column=0, pady=6)
    spin_start_hour = tk.Spinbox(form_frame, from_=0, to=23, width=5, format="%02.0f")
    spin_start_min = tk.Spinbox(form_frame, from_=0, to=59, width=5, format="%02.0f")
    spin_start_hour.grid(row=5, column=1, sticky="w", padx=(0, 50))
    spin_start_min.grid(row=5, column=1, sticky="e")

    # Giờ kết thúc
    tk.Label(form_frame, text="Giờ kết thúc (HH:mm):", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=6, column=0, pady=6)
    spin_end_hour = tk.Spinbox(form_frame, from_=0, to=23, width=5, format="%02.0f")
    spin_end_min = tk.Spinbox(form_frame, from_=0, to=59, width=5, format="%02.0f")
    spin_end_hour.grid(row=6, column=1, sticky="w", padx=(0, 50))
    spin_end_min.grid(row=6, column=1, sticky="e")

    # Học kỳ - năm học
    tk.Label(form_frame, text="Học kỳ - Năm học:", font=LABEL_FONT, width=18, anchor="e", bg=FORM_BG_COLOR, fg="white").grid(row=7, column=0, pady=6)
    combo_hk = ttk.Combobox(form_frame, font=("Arial", 10), width=33, state="readonly", values=hk_list)
    combo_hk.grid(row=7, column=1, pady=6)

    # Tổng điểm cộng - NHÉT VÀO FORM_FRAME
    diem_label = tk.Label(
        form_frame,
        text="➞ Tổng điểm cộng: 0",
        font=("Arial", 11, "bold"),
        fg="green",
        bg=FORM_BG_COLOR,
        anchor="w"
    )
    diem_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=(10, 5))

    # Nút tạo hoạt động - CŨNG NHÉT VÀO FORM_FRAME
    btn_create = tk.Button(
        form_frame,
        text="Tạo hoạt động",
        command=tao_hoat_dong,
        **CREATE_BUTTON_STYLE
    )
    btn_create.grid(row=9, column=0, columnspan=2, pady=(20, 10))
