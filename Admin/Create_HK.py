import tkinter as tk
from tkinter import messagebox
import sqlite3
from Admin.Styles_admin import *
from Database.Create_db import DB_NAME


def render_create_hoc_ky(container):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg=PAGE_BG_COLOR)
    tk.Label(container, text="📘 Tạo học kỳ", font=TITLE_FONT, bg="white", fg="#003366").pack(
        anchor="w", padx=28, pady=(20, 5))

    def them_hoc_ky():
        name_hk = entry_name_hk.get().strip()
        school_year = entry_school_year.get().strip()

        if not name_hk or not school_year:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên học kỳ và năm học.")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # Kiểm tra trùng
            cursor.execute("SELECT * FROM HK_NK WHERE NAME_HK = ? AND SCHOOL_YEAR = ?", (name_hk, school_year))
            if cursor.fetchone():
                messagebox.showerror("Trùng học kỳ", f"Học kỳ {name_hk} năm {school_year} đã tồn tại!")
                return

            # Tự động sinh ID_HK tăng dần
            cursor.execute("SELECT MAX(ID_HK) FROM HK_NK")
            max_id = cursor.fetchone()[0]
            next_id = (max_id + 1) if max_id else 1

            # Thêm học kỳ mới
            cursor.execute("INSERT INTO HK_NK (ID_HK, NAME_HK, SCHOOL_YEAR) VALUES (?, ?, ?)",
                           (next_id, name_hk, school_year))
            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", f"Đã thêm học kỳ {name_hk} ({school_year}) thành công!")
            entry_name_hk.delete(0, tk.END)
            entry_school_year.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def back_to_main():
        from Admin.Admin_main import render_admin_main
        render_admin_main(container.master)

    # ========== GIAO DIỆN ==========
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

    # Tên học kỳ
    tk.Label(form_inner, text="Tên học kỳ (ví dụ: HK1):", font=LABEL_FONT, anchor="e",
             bg=FORM_BG_COLOR, fg="white", width=22).grid(row=0, column=0, sticky="e", pady=6)
    entry_name_hk = tk.Entry(form_inner, **ENTRY_STYLE_ACTIVITY)
    entry_name_hk.grid(row=0, column=1, pady=6)

    # Năm học
    tk.Label(form_inner, text="Năm học (ví dụ: 2024-2025):", font=LABEL_FONT, anchor="e",
             bg=FORM_BG_COLOR, fg="white", width=22).grid(row=1, column=0, sticky="e", pady=6)
    entry_school_year = tk.Entry(form_inner, **ENTRY_STYLE_ACTIVITY)
    entry_school_year.grid(row=1, column=1, pady=6)

    # Nút tạo
    btn_back = tk.Button(
        form_inner,
        text="← Quay lại",
        command=back_to_main,
        **BACK_BUTTON_STYLE
    )
    btn_back.grid(row=2, column=0, pady=(20, 10), sticky="w", padx=(0, 10))

    btn_create = tk.Button(
        form_inner,
        text="Thêm học kỳ",
        command=them_hoc_ky,
        **CREATE_BUTTON_STYLE
    )
    btn_create.grid(row=2, column=1, pady=(20, 10), sticky="e")