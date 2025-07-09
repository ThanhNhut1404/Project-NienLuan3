import tkinter as tk
from tkinter import messagebox
import json

from Admin.Styles_admin import TITLE_FONT, LABEL_FONT, ENTRY_FONT, BUTTON_STYLE
from Database.Create_db import (
    insert_sinh_vien,
    sinh_vien_exists,
    get_all_sinh_vien,
    create_table_sinh_vien
)
from Admin.face_util import capture_multiple_encodings, compare_face


def render_student_create(container):
    for widget in container.winfo_children():
        widget.destroy()

    create_table_sinh_vien()
    container.config(bg="white")
    form = tk.Frame(container, bg="white")
    form.pack(pady=20)

    def show_popup(message):
        popup = tk.Toplevel()
        popup.title("Thông báo")
        popup.geometry("300x120")
        popup.resizable(False, False)
        tk.Label(popup, text=message, wraplength=280, justify="center", fg="red").pack(pady=15)
        tk.Button(popup, text="OK", command=popup.destroy, bg="#f44336", fg="white", width=10).pack(pady=5)
        popup.grab_set()

    def register_sinh_vien():
        name = name_entry.get().strip()
        mssv = mssv_entry.get().strip()
        email = email_entry.get().strip()
        birthdate = birth_entry.get().strip()
        gender = gender_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip()
        class_sv = class_entry.get().strip()
        password = password_entry.get().strip()

        if not all([name, mssv, email, birthdate, gender, phone, address, class_sv, password]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tất cả các trường.")
            return

        # Kiểm tra trùng tên
        if sinh_vien_exists(name):
            messagebox.showerror("Đã tồn tại", f"Tên '{name}' đã tồn tại. Vui lòng chọn tên khác.")
            return

        # Kiểm tra trùng email hoặc MSSV
        existing = get_all_sinh_vien()
        for sv in existing:
            if sv['name'] == name or sv.get('email') == email or sv.get('mssv') == mssv:
                messagebox.showerror("Trùng thông tin", "Email hoặc MSSV đã tồn tại.")
                return

        # Chụp ảnh
        encodings = capture_multiple_encodings()
        if not encodings:
            messagebox.showerror("Lỗi", "Không lấy được dữ liệu khuôn mặt.")
            return

        # Kiểm tra trùng khuôn mặt
        for encoding in encodings:
            matched = compare_face(encoding, existing)
            if matched:
                show_popup(f"Gương mặt đã tồn tại: {matched['name']}")
                return

        try:
            encoding_json = json.dumps(encodings)
            insert_sinh_vien(name, mssv, email, address, birthdate, gender, class_sv, password, encoding_json)
            messagebox.showinfo("Thành công", f"Đăng ký {name} thành công với {len(encodings)} ảnh.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")

    # Tạo label + entry
    def make_label(text, row):
        tk.Label(form, text=text, font=LABEL_FONT, bg="white").grid(row=row, column=0, sticky='e', padx=10, pady=5)

    def make_entry(row, show=None):
        e = tk.Entry(form, font=ENTRY_FONT, width=30, show=show)
        e.grid(row=row, column=1, padx=10, pady=5)
        return e

    make_label("Họ tên:", 0)
    name_entry = make_entry(0)

    make_label("MSSV:", 1)
    mssv_entry = make_entry(1)

    make_label("Email:", 2)
    email_entry = make_entry(2)

    make_label("Ngày sinh (YYYY-MM-DD):", 3)
    birth_entry = make_entry(3)

    make_label("Giới tính (0 = Nam / 1 = Nữ):", 4)
    gender_entry = make_entry(4)

    make_label("Số điện thoại:", 5)
    phone_entry = make_entry(5)

    make_label("Địa chỉ:", 6)
    address_entry = make_entry(6)

    make_label("Lớp:", 7)
    class_entry = make_entry(7)

    make_label("Mật khẩu:", 8)
    password_entry = make_entry(8, show="*")

    tk.Button(
        form,
        text="Đăng ký khuôn mặt",
        command=register_sinh_vien,
        **BUTTON_STYLE
    ).grid(row=9, column=0, columnspan=2, pady=15)
