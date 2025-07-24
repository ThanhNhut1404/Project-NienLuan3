import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import sqlite3
import os
from PIL import Image, ImageTk
from datetime import datetime
from Database.Create_db import DB_NAME
import hashlib

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

    # ===== GIAO DIỆN CHÍNH =====
    title_label = tk.Label(container, text="📝 Cập nhật thông tin sinh viên", font=("Segoe UI", 18, "bold"), fg="#2C387E", bg="white")
    title_label.pack(pady=(20, 10))

    form_frame = tk.Frame(container, bg="#F5F5F5", bd=2, relief="groove")
    form_frame.pack(pady=10, padx=20)

    def create_label_entry(row, text, entry_var, show=None):
        tk.Label(form_frame, text=text, bg="#F5F5F5", font=("Segoe UI", 11)).grid(row=row, column=0, sticky='e', padx=10, pady=5)
        entry = tk.Entry(form_frame, textvariable=entry_var, width=30, show=show, font=("Segoe UI", 10))
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    # ===== CÁC TRƯỜNG =====
    tk.Label(form_frame, text="Ngày sinh:", bg="#F5F5F5", font=("Segoe UI", 11)).grid(row=0, column=0, sticky='e', padx=10, pady=5)
    entry_birth = DateEntry(form_frame, date_pattern="dd-mm-yyyy", width=27, font=("Segoe UI", 10))
    try:
        entry_birth.set_date(datetime.strptime(birth, "%Y-%m-%d"))
    except:
        pass
    entry_birth.grid(row=0, column=1, pady=5, padx=10)

    address_var = tk.StringVar(value=address or "")
    phone_var = tk.StringVar(value=phone or "")
    old_pw_var = tk.StringVar()
    new_pw_var = tk.StringVar()

    create_label_entry(1, "Địa chỉ:", address_var)
    create_label_entry(2, "Số điện thoại:", phone_var)
    old_pw_entry = create_label_entry(3, "Mật khẩu cũ:", old_pw_var, show="*")
    new_pw_entry = create_label_entry(4, "Mật khẩu mới:", new_pw_var, show="*")

    # ===== HIỆN MẬT KHẨU =====
    def toggle_password():
        show = '' if show_pw_var.get() else '*'
        old_pw_entry.config(show=show)
        new_pw_entry.config(show=show)

    show_pw_var = tk.BooleanVar()
    tk.Checkbutton(
        form_frame, text="Hiện mật khẩu", variable=show_pw_var, command=toggle_password,
        bg="#F5F5F5", font=("Segoe UI", 10)
    ).grid(row=5, column=1, sticky="w", padx=10)

    # ===== CHỌN ẢNH =====
    def choose_image():
        nonlocal img_file_path
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            img_file_path = file_path
            show_image(file_path)

    def show_image(path):
        try:
            img = Image.open(path)
            img = img.resize((100, 120))
            img_tk = ImageTk.PhotoImage(img)
            img_label.config(image=img_tk)
            img_label.image = img_tk
        except:
            pass

    tk.Button(form_frame, text="Chọn ảnh đại diện", command=choose_image, font=("Segoe UI", 10), relief="solid", bd=1, bg="white").grid(row=6, column=0, columnspan=2, pady=10)
    img_label = tk.Label(form_frame, bg="#F5F5F5")
    img_label.grid(row=7, column=0, columnspan=2)
    if img_path and os.path.exists(img_path):
        show_image(img_path)

    # ===== LƯU THAY ĐỔI =====
    def save_changes():
        new_address = address_var.get().strip()
        new_phone = phone_var.get().strip()
        new_birth = entry_birth.get_date().strftime("%d-%m-%Y")
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
            on_back()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Cập nhật thất bại: {str(e)}")

    save_btn = tk.Button(
        container, text="✔ Cập nhật thông tin", command=save_changes,
        font=("Segoe UI", 11, "bold"), bg="#2E8B57", fg="white",
        activebackground="#246b45", activeforeground="white",
        relief="flat", bd=0, padx=15, pady=7
    )
    save_btn.pack(pady=15)

    def on_enter(e): save_btn.config(bg="#246b45")
    def on_leave(e): save_btn.config(bg="#2E8B57")
    save_btn.bind("<Enter>", on_enter)
    save_btn.bind("<Leave>", on_leave)

    # ===== QUAY LẠI =====
    tk.Button(
        container, text="⬅ Quay lại", command=on_back,
        font=("Segoe UI", 10), bg="#ddd", relief="flat", padx=10, pady=5
    ).pack()