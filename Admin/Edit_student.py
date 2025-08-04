import tkinter as tk
from tkinter import messagebox
from Admin.Styles_admin import *
from Database.Create_db import update_sinh_vien
import datetime

def render_student_edit(container, student_data):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg=PAGE_BG_COLOR)
    tk.Label(container, text="🖉 Chỉnh sửa thông tin sinh viên", font=TITLE_FONT, bg="white", fg="#003366").pack(anchor="w", padx=28, pady=(20, 5))

    outer_frame = tk.Frame(
        container,
        bg=FORM_BG_COLOR,
        bd=FORM_BORDER_WIDTH,
        relief=FORM_BORDER_STYLE,
        width=480,
    )
    outer_frame.pack(pady=10)

    form_frame = tk.Frame(outer_frame, bg=FORM_BG_COLOR)
    form_frame.pack(padx=FORM_PADDING_X, pady=FORM_PADDING_Y)

    def create_row(label, value, row):
        tk.Label(form_frame, text=label, font=LABEL_FONT, bg="#003366", fg="white").grid(row=row, column=0, sticky="e", padx=10, pady=8)
        entry = tk.Entry(form_frame, font=ENTRY_FONT, width=35)
        entry.insert(0, value)
        entry.grid(row=row, column=1, padx=10, pady=8)
        return entry

    name_entry = create_row("Họ và tên:", student_data['name'], 0)
    class_entry = create_row("Lớp:", student_data['class'], 1)
    mssv_entry = create_row("MSSV:", student_data['mssv'], 2)

    # Giới tính
    tk.Label(form_frame, text="Giới tính:", font=LABEL_FONT, bg="#003366", fg="white") \
        .grid(row=3, column=0, sticky="e", padx=10, pady=8)
    gender_var = tk.IntVar(value=1 if str(student_data['sex']) == "1" else 0)
    gender_frame = tk.Frame(form_frame, bg="#003366")
    gender_frame.grid(row=3, column=1, sticky="w")
    for text, val in [("Nam", 1), ("Nữ", 0)]:
        tk.Radiobutton(
            gender_frame, text=text, variable=gender_var, value=val,
            bg="#003366", fg="white", font=ENTRY_FONT,
            selectcolor="black", activebackground="#003366", activeforeground="white"
        ).pack(side="left", padx=(0, 10))

    birth_entry = create_row("Ngày sinh:", student_data['date'], 4)
    address_entry = create_row("Địa chỉ:", student_data['address'], 5)
    email_entry = create_row("Email:", student_data['email'], 6)
    phone_entry = create_row("Số điện thoại:", student_data.get('phone', ""), 7)
    password_entry = create_row("Mật khẩu:", student_data['password'], 8)

    # ✅ Đặt sau khi các biến đã có
    def save_changes():
        name = name_entry.get().strip()
        mssv = mssv_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()
        birth = birth_entry.get().strip()
        sex = gender_var.get()
        class_sv = class_entry.get().strip()
        password = password_entry.get().strip()
        phone = phone_entry.get().strip()

        if not all([name, mssv, email, class_sv, password, birth, phone]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        try:
            datetime.datetime.strptime(birth, "%d-%m-%Y")
        except:
            messagebox.showerror("Lỗi", "Ngày sinh không hợp lệ. Định dạng đúng: dd-mm-yyyy")
            return

        try:
            update_sinh_vien(student_data['id'], name, mssv, email, address, birth, sex, class_sv, password, phone)
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin sinh viên.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # Nút "Quay lại" và "Lưu thay đổi" nằm cùng 1 hàng
    def back_to_list():
        from Admin.List_student import render_student_list
        render_student_list(container, back_to_list)

    btn_back = tk.Button(
        form_frame,
        text="← Quay lại",
        command=back_to_list,
        **BACK_BUTTON_STYLE
    )
    btn_back.grid(row=9, column=0, pady=(20, 10), sticky="w", padx=(10, 5))

    # Nút "Cập nhật" ở cột 1, canh phải
    btn_save = tk.Button(
        form_frame,
        text="Cập nhật",
        command=save_changes,
        **BUTTON_STYLE
    )
    btn_save.grid(row=9, column=1, pady=(20, 10), sticky="e", padx=(5, 10))

