import tkinter as tk
from tkinter import messagebox
from Admin.Styles_admin import LABEL_FONT, ENTRY_FONT, BUTTON_STYLE
from Database.Create_db import update_sinh_vien
import datetime

def render_student_edit(container, student_data):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg="white")

    tk.Label(container, text="📝 Chỉnh sửa thông tin sinh viên", font=("Arial", 18, "bold"), fg="#003366", bg="white") \
        .pack(pady=20)

    form_frame = tk.Frame(container, bg="white")
    form_frame.pack(pady=10)

    def create_row(label, value, row):
        tk.Label(form_frame, text=label, font=LABEL_FONT, bg="white").grid(row=row, column=0, sticky="e", padx=10, pady=8)
        entry = tk.Entry(form_frame, font=ENTRY_FONT, width=35)
        entry.insert(0, value)
        entry.grid(row=row, column=1, padx=10, pady=8)
        return entry

    name_entry = create_row("Họ tên:", student_data['name'], 0)
    mssv_entry = create_row("MSSV:", student_data['mssv'], 1)
    email_entry = create_row("Email:", student_data['email'], 2)
    address_entry = create_row("Địa chỉ:", student_data['address'], 3)
    birth_entry = create_row("Ngày sinh (YYYY-MM-DD):", student_data['date'], 4)

    # Giới tính
    tk.Label(form_frame, text="Giới tính:", font=LABEL_FONT, bg="white").grid(row=5, column=0, sticky="e", padx=10, pady=8)
    gender_var = tk.IntVar(value=1 if str(student_data['sex']) == "1" else 0)
    gender_frame = tk.Frame(form_frame, bg="white")
    gender_frame.grid(row=5, column=1, sticky="w")
    tk.Radiobutton(gender_frame, text="Nam", variable=gender_var, value=1, bg="white", font=ENTRY_FONT).pack(side="left")
    tk.Radiobutton(gender_frame, text="Nữ", variable=gender_var, value=0, bg="white", font=ENTRY_FONT).pack(side="left")

    class_entry = create_row("Lớp:", student_data['class'], 6)
    password_entry = create_row("Mật khẩu:", student_data['password'], 7)

    def save_changes():
        name = name_entry.get().strip()
        mssv = mssv_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()
        birth = birth_entry.get().strip()
        sex = gender_var.get()
        class_sv = class_entry.get().strip()
        password = password_entry.get().strip()

        if not all([name, mssv, email, class_sv, password, birth]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin bắt buộc.")
            return

        try:
            datetime.datetime.strptime(birth, "%Y-%m-%d")
        except:
            messagebox.showerror("Lỗi", "Ngày sinh không hợp lệ. Định dạng: YYYY-MM-DD")
            return

        try:
            update_sinh_vien(student_data['id'], name, mssv, email, address, birth, sex, class_sv, password)
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin sinh viên.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def back_to_list():
        from Admin.List_student import render_student_list
        render_student_list(container)

    tk.Button(container, text="💾 Lưu thay đổi", command=save_changes, **BUTTON_STYLE).pack(pady=20)
    tk.Button(container, text="⬅️ Quay lại danh sách", command=back_to_list, **BUTTON_STYLE).pack(pady=(0, 20))
