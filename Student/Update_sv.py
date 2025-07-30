import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import sqlite3
import os
from PIL import Image, ImageTk
from datetime import datetime
import hashlib
from Database.Create_db import DB_NAME
from Student.Styles_student import *

def render_update_sv(container, user, go_back):
    def on_back():
        if go_back:
            go_back()

    for widget in container.winfo_children():
        widget.destroy()

    mssv = user.get('MSSV') or user.get('mssv')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SINH_VIEN WHERE MSSV = ?", (mssv,))
    sv = cursor.fetchone()
    conn.close()

    if not sv:
        messagebox.showerror("Lỗi", "Không tìm thấy sinh viên.")
        return

    id_sv, name, mssv, email, address, birth, sex, lop, phone, password_sv, tong_diem_hd, face_encoding, img_path, created_at = sv
    img_file_path = img_path

    title_label = tk.Label(container, text="🔄 Cập nhật thông tin sinh viên", font=TITLE_FONT, fg="#00897B", bg="white")
    title_label.pack(anchor="w", padx=60, pady=(20, 10))

    outer_frame = tk.Frame(container, bg="#F5F5F5", bd=0)
    outer_frame.pack(pady=30)
    outer_frame.pack_propagate(False)
    outer_frame.config(height=500, width=700)

    left_frame = tk.Frame(outer_frame, bg="#F5F5F5")
    left_frame.grid(row=0, column=0, padx=(20, 40), pady=20, sticky="n")

    right_frame = tk.Frame(outer_frame, bg="#F5F5F5")
    right_frame.grid(row=0, column=1, padx=30, pady=20, sticky="nw")

    def choose_image():
        nonlocal img_file_path
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            img_file_path = file_path
            show_image(file_path)

    def show_image(path):
        try:
            img = Image.open(path)
            img = img.resize((180, 210))
            img_tk = ImageTk.PhotoImage(img)
            img_label.config(image=img_tk)
            img_label.image = img_tk
        except:
            pass

    img_label = tk.Label(left_frame, bg="#F5F5F5")
    img_label.pack(pady=(0, 10))

    # Dùng ảnh từ img_path nếu có, nếu không thì dùng avatar mặc định
    if img_path and os.path.exists(img_path):
        try:
            img = Image.open(img_path)
        except:
            img = Image.new("RGB", (180, 210), color="#cccccc")
    else:
        # Dùng ảnh mờ mặc định
        try:
            img = Image.open("avatar.png")
        except:
            img = Image.new("RGB", (180, 210), color="#cccccc")  # fallback nếu thiếu avatar.png

    # Resize ảnh
    img = img.resize((180, 210))
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk

    choose_img_label = tk.Label(
        left_frame,
        text="Chọn ảnh",
        fg="#1a73e8",
        bg="#F5F5F5",
        cursor="hand2",
        font=("Arial", 11,)
    )
    choose_img_label.pack(pady=(0, 0))
    choose_img_label.bind("<Button-1>", lambda e: choose_image())

    form_frame = tk.Frame(right_frame, bg="#F5F5F5", pady=15)
    form_frame.pack(anchor="w", fill="both", expand=True)  # 👈 Giúp đẩy nút xuống dưới cùng

    def create_label_entry(row, text, entry_var, show=None):
        tk.Label(form_frame, text=text, bg="#F5F5F5", fg="#00897B", font=LABEL_FONT) \
            .grid(row=row, column=0, sticky='e', padx=10, pady=6)
        entry = tk.Entry(form_frame, textvariable=entry_var, width=25, show=show, font=ENTRY_FONT, bg="white")
        entry.grid(row=row, column=1, padx=10, pady=6, sticky='w')
        return entry

    # Ngày sinh
    tk.Label(form_frame, text="Ngày sinh:", bg="#F5F5F5", fg="#00897B", font=LABEL_FONT) \
        .grid(row=0, column=0, sticky='e', padx=10, pady=6)

    entry_birth = DateEntry(form_frame, date_pattern="dd-mm-yyyy", width=23, font=ENTRY_FONT)

    # Gán ngày sinh nếu có
    # Gán ngày sinh nếu có
    if birth:
        try:
            parsed_birth = datetime.strptime(birth, "%Y-%m-%d")  # ← đây là dòng cần sửa
            entry_birth.set_date(parsed_birth)
        except Exception as e:
            print(f"[⚠️] Không thể đặt ngày sinh từ DB: {birth} → {e}")

    entry_birth.grid(row=0, column=1, padx=10, pady=6, sticky="w")

    address_var = tk.StringVar(value=address or "")
    phone_var = tk.StringVar(value=phone or "")
    old_pw_var = tk.StringVar()
    new_pw_var = tk.StringVar()

    old_pw_entry = create_label_entry(1, "Địa chỉ:", address_var)
    create_label_entry(2, "Số điện thoại:", phone_var)
    old_pw_entry = create_label_entry(3, "Mật khẩu cũ:", old_pw_var, show="*")
    new_pw_entry = create_label_entry(4, "Mật khẩu mới:", new_pw_var, show="*")

    tk.Label(form_frame, text="*Để trống nếu không muốn đổi mật khẩu",
             fg="red", bg="#F5F5F5", font=("Arial", 9, "italic")) \
        .grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 4))

    def toggle_password():
        show = '' if show_pw_var.get() else '*'
        old_pw_entry.config(show=show)
        new_pw_entry.config(show=show)

    show_pw_var = tk.BooleanVar()

    check_btn = tk.Checkbutton(
        form_frame,
        text="Hiện mật khẩu",
        variable=show_pw_var,
        command=toggle_password,
        bg="#F5F5F5",  # Nền xung quanh
        activebackground="#F5F5F5",
        fg="black",  # Màu chữ
        relief="flat",
        activeforeground="black",
        selectcolor="#00897B",
        overrelief="flat",
        font=ENTRY_FONT
    )
    check_btn.grid(row=6, column=1, sticky="w", padx=10)

    def save_changes():
        new_address = address_var.get().strip()
        new_phone = phone_var.get().strip()
        new_birth = entry_birth.get_date().strftime("%Y-%m-%d")
        old_pw = old_pw_var.get().strip()
        new_pw = new_pw_var.get().strip()

        if old_pw:
            if hashlib.sha256(old_pw.encode()).hexdigest() != password_sv:
                messagebox.showerror("Sai mật khẩu", "Mật khẩu cũ không đúng.")
                return
            if len(new_pw) < 9 or not any(c.isupper() for c in new_pw) or not any(c.isdigit() for c in new_pw):
                messagebox.showwarning("Mật khẩu yếu", "Mật khẩu mới phải có ít nhất 9 ký tự, gồm chữ hoa và số.")
                return
            hashed_pw = hashlib.sha256(new_pw.encode()).hexdigest()
        else:
            hashed_pw = password_sv

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE SINH_VIEN
                SET ADDRESS_SV = ?, PHONE_SV = ?, DATE_SV = ?, PASSWORD_SV = ?, IMG = ?
                WHERE MSSV = ?
            ''', (new_address, new_phone, new_birth, hashed_pw, img_file_path, mssv))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")

            # ✅ Cập nhật dữ liệu user để View_infor hiển thị đúng
            user["address"] = new_address
            user["phone"] = new_phone
            user["date"] = entry_birth.get_date().strftime("%d-%m-%Y")
            user["img"] = img_file_path  # Quan trọng nhất: cập nhật ảnh

            on_back()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Cập nhật thất bại: {str(e)}")

    # Các nút dưới cùng
    button_frame = tk.Frame(outer_frame, bg="#F5F5F5")
    button_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=40, pady=(0, 10))  # 👈 Gần sát đáy

    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    back_btn = tk.Button(button_frame, text="← Quay lại", command=on_back, **BACK_BUTTON_UPDATE_STYLE)
    back_btn.grid(row=0, column=0, sticky="w")

    save_btn = tk.Button(button_frame, text="Cập nhật thông tin", command=save_changes, **BUTTON_UPDATE_STYLE)
    save_btn.grid(row=0, column=1, sticky="e", padx=(0, 90))
