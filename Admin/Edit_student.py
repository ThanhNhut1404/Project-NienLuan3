import tkinter as tk
from tkinter import messagebox
import re
import hashlib
from Admin.Styles_admin import *
from Database.Create_db import update_sinh_vien
import datetime


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def render_student_edit(container, student_data):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg=PAGE_BG_COLOR)
    tk.Label(container, text="🖉 Chỉnh sửa thông tin sinh viên", font=TITLE_FONT, bg="white", fg="#003366").pack(
        anchor="w", padx=28, pady=(20, 5))

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

    def create_row(label, value, row, show=None):
        tk.Label(form_frame, text=label, font=LABEL_FONT, bg="#003366", fg="white").grid(row=row, column=0, sticky="e",
                                                                                         padx=10, pady=8)
        entry = tk.Entry(form_frame, font=ENTRY_FONT, width=35, show=show)
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

    # Mật khẩu với tùy chọn hiển thị
    password_entry = create_row("Mật khẩu:", "", 8, show="*")  # Không hiển thị mật khẩu đã hash
    show_password_var = tk.BooleanVar(value=False)

    def toggle_password():
        password_entry.config(show="" if show_password_var.get() else "*")

    tk.Checkbutton(
        form_frame,
        text="Hiện mật khẩu",
        variable=show_password_var,
        command=toggle_password,
        bg="#003366", fg="white", font=ENTRY_FONT,
        selectcolor="black", activebackground="#003366", activeforeground="white"
    ).grid(row=9, column=1, sticky="w", padx=10, pady=(0, 10))

    def save_changes():
        name = name_entry.get().strip()
        mssv = mssv_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()
        birth = birth_entry.get().strip()
        sex = gender_var.get()
        class_sv = class_entry.get().strip()
        raw_password = password_entry.get().strip()
        phone = phone_entry.get().strip()

        if not all([name, mssv, email, class_sv, birth, phone]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        # Kiểm tra định dạng ngày sinh
        try:
            datetime.datetime.strptime(birth, "%d-%m-%Y")
        except:
            messagebox.showerror("Lỗi", "Ngày sinh không hợp lệ. Định dạng đúng: dd-mm-yyyy")
            return

        # Kiểm tra định dạng email
        if not re.match(r'^[\w\.-]+@gmail\.com$', email):
            messagebox.showwarning("Lỗi định dạng Email", "Email phải có định dạng hợp lệ và kết thúc bằng @gmail.com")
            return

        # Kiểm tra số điện thoại
        if not re.match(r'^0\d{9}$', phone):
            messagebox.showwarning("Lỗi Số điện thoại", "Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0.")
            return

        # Kiểm tra họ và tên
        if not re.match(r"^[A-Za-zÀ-ỹ\s]+$", name):
            messagebox.showwarning("Lỗi họ tên", "Họ tên chỉ được chứa chữ cái và khoảng trắng.")
            return
        if len(name.split()) < 2:
            messagebox.showwarning("Lỗi họ tên", "Vui lòng nhập đầy đủ họ và tên.")
            return

        # Kiểm tra địa chỉ
        if len(address) < 5:
            messagebox.showwarning("Lỗi địa chỉ", "Địa chỉ quá ngắn, vui lòng nhập đầy đủ.")
            return

        # Kiểm tra mật khẩu nếu người dùng nhập mật khẩu mới
        if raw_password:
            if len(raw_password) < 6:
                messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu phải có ít nhất 6 ký tự.")
                return
            if not re.search(r'[A-Z]', raw_password):
                messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu phải chứa ít nhất 1 chữ cái in hoa.")
                return
            if not re.search(r'[a-z]', raw_password):
                messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu phải chứa ít nhất 1 chữ cái thường.")
                return
            if not re.search(r'\d', raw_password):
                messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu phải chứa ít nhất 1 số.")
                return
            if " " in raw_password:
                messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu không được chứa khoảng trắng.")
                return
            password = hash_password(raw_password)
        else:
            # Nếu không nhập mật khẩu mới, giữ nguyên mật khẩu cũ
            password = student_data['password']

        try:
            update_sinh_vien(student_data['id'], name, mssv, email, address, birth, sex, class_sv, password, phone)
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin sinh viên.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def back_to_list():
        from Admin.List_student import render_student_list
        render_student_list(container, back_to_list)

    btn_back = tk.Button(
        form_frame,
        text="← Quay lại",
        command=back_to_list,
        **BACK_BUTTON_STYLE
    )
    btn_back.grid(row=10, column=0, pady=(20, 10), sticky="w", padx=(10, 5))

    btn_save = tk.Button(
        form_frame,
        text="Cập nhật",
        command=save_changes,
        **BUTTON_STYLE
    )
    btn_save.grid(row=10, column=1, pady=(20, 10), sticky="e", padx=(5, 10))