import tkinter as tk
from tkinter import messagebox
import sqlite3
from Admin.Styles_admin import *
from Database.Create_db import DB_NAME


def render_edit_hk(container, hoc_ky_data, go_back_to_list_view):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg=PAGE_BG_COLOR)

    tk.Label(container, text="✍️ Sửa học kỳ", font=TITLE_FONT, bg="white", fg="#003366").pack(
        anchor="w", padx=28, pady=(20, 5))

    id_hk = hoc_ky_data[0]
    current_name = hoc_ky_data[1]
    current_year = hoc_ky_data[2]

    # ====== Hàm cập nhật học kỳ ======
    def cap_nhat_hoc_ky():
        name_hk = entry_name_hk.get().strip()
        school_year = entry_school_year.get().strip()

        if not name_hk or not school_year:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên học kỳ và năm học.")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # Kiểm tra trùng học kỳ (loại trừ chính nó)
            cursor.execute("SELECT * FROM HK_NK WHERE NAME_HK = ? AND SCHOOL_YEAR = ? AND ID_HK != ?",
                           (name_hk, school_year, id_hk))
            if cursor.fetchone():
                messagebox.showerror("Trùng học kỳ", f"Học kỳ {name_hk} - {school_year} đã tồn tại.")
                return

            # Cập nhật
            cursor.execute("UPDATE HK_NK SET NAME_HK = ?, SCHOOL_YEAR = ? WHERE ID_HK = ?",
                           (name_hk, school_year, id_hk))
            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Cập nhật học kỳ thành công!")

            # Quay về danh sách sau khi cập nhật
            back_to_list()

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== Hàm quay lại ======
    def back_to_list():
        go_back_to_list_view()

    # ====== GIAO DIỆN ======
    outer_frame = tk.Frame(container, bg=FORM_BG_COLOR,
                           bd=FORM_BORDER_WIDTH, relief=FORM_BORDER_STYLE, width=480)
    outer_frame.pack(pady=10)

    form_frame = tk.Frame(outer_frame, bg=FORM_BG_COLOR)
    form_frame.pack(padx=FORM_PADDING_X, pady=FORM_PADDING_Y)

    form_inner = tk.Frame(form_frame, bg=FORM_BG_COLOR)
    form_inner.pack()

    # Tên học kỳ
    tk.Label(form_inner, text="Tên học kỳ (vd: Học kỳ 1):", font=LABEL_FONT, anchor="e",
             bg=FORM_BG_COLOR, fg="white", width=22).grid(row=0, column=0, sticky="e", pady=6)
    entry_name_hk = tk.Entry(form_inner, **ENTRY_STYLE_ACTIVITY)
    entry_name_hk.insert(0, current_name)
    entry_name_hk.grid(row=0, column=1, pady=6)

    # Năm học
    tk.Label(form_inner, text="Năm học (vd: 2024-2025):", font=LABEL_FONT, anchor="e",
             bg=FORM_BG_COLOR, fg="white", width=22).grid(row=1, column=0, sticky="e", pady=6)
    entry_school_year = tk.Entry(form_inner, **ENTRY_STYLE_ACTIVITY)
    entry_school_year.insert(0, current_year)
    entry_school_year.grid(row=1, column=1, pady=6)

    # Nút quay lại
    btn_back = tk.Button(form_inner, text="← Quay lại",
                         command=back_to_list, **BACK_BUTTON_STYLE)
    btn_back.grid(row=2, column=0, pady=(20, 10), sticky="w", padx=(0, 10))

    # Nút lưu chỉnh sửa
    btn_update = tk.Button(form_inner, text="Lưu chỉnh sửa",
                           command=cap_nhat_hoc_ky, **CREATE_BUTTON_STYLE)
    btn_update.grid(row=2, column=1, pady=(20, 10), sticky="e")
