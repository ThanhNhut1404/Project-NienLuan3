import tkinter as tk
from tkinter import messagebox
import sqlite3
from Database.Create_db import DB_NAME

def render_create_hoc_ky(container):
    for widget in container.winfo_children():
        widget.destroy()

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

    # ========== GIAO DIỆN ==========
    tk.Label(container, text="📘 TẠO HỌC KỲ MỚI", font=("Arial", 16, "bold"), fg="#003366").pack(pady=10)

    form = tk.Frame(container, padx=20, pady=20, bg="#f2f2f2")
    form.pack()

    # Tên học kỳ
    tk.Label(form, text="Tên học kỳ (ví dụ: HK1):", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5)
    entry_name_hk = tk.Entry(form, font=("Arial", 10), width=30)
    entry_name_hk.grid(row=0, column=1, pady=5)

    # Năm học
    tk.Label(form, text="Năm học (ví dụ: 2024-2025):", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
    entry_school_year = tk.Entry(form, font=("Arial", 10), width=30)
    entry_school_year.grid(row=1, column=1, pady=5)

    # Nút tạo
    tk.Button(container, text="Thêm học kỳ", font=("Arial", 11, "bold"),
              bg="#006699", fg="white", width=20, command=them_hoc_ky).pack(pady=15)
