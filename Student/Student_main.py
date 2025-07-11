import tkinter as tk
from tkinter import messagebox
import json
import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageTk

from Database.Create_db import get_all_sinh_vien
from Student.Styles_student import LABEL_FONT, ENTRY_FONT, BUTTON_STYLE

def render_student_main(container, user):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg="#f0f0f0")

    # Tiêu đề hiển thị tên sinh viên
    header_text = f"TRANG CHÍNH SINH VIÊN - {user.get('name', '')}"
    header = tk.Label(container, text=header_text, font=("Arial", 18, "bold"), bg="#4CAF50", fg="white")
    header.pack(fill="x")

    # Nội dung chính
    content_frame = tk.Frame(container, bg="#f0f0f0")
    content_frame.pack(expand=True, fill="both", pady=20)

    welcome_label = tk.Label(
        content_frame,
        text=f"Chào mừng {user.get('name', 'bạn')} đến với hệ thống!",
        font=("Arial", 14),
        bg="#f0f0f0"
    )
    welcome_label.pack(pady=10)

    # Nút chức năng cơ bản
    btn_frame = tk.Frame(content_frame, bg="#f0f0f0")
    btn_frame.pack(pady=10)

    btn_view_profile = tk.Button(
        btn_frame,
        text="Xem thông tin",
        command=lambda: messagebox.showinfo("Thông tin", json.dumps(user, indent=2, ensure_ascii=False)),
        **BUTTON_STYLE
    )
    btn_view_profile.grid(row=0, column=0, padx=10, pady=5)

    btn_view_grades = tk.Button(
        btn_frame,
        text="Xem điểm",
        command=lambda: messagebox.showinfo("Điểm", "Hiển thị điểm..."),
        **BUTTON_STYLE
    )
    btn_view_grades.grid(row=0, column=1, padx=10, pady=5)

    btn_logout = tk.Button(
        btn_frame,
        text="Đăng xuất",
        command=lambda: (messagebox.showinfo("Đăng xuất", "Bạn đã đăng xuất."), container.master.destroy()),
        **BUTTON_STYLE
    )
    btn_logout.grid(row=1, column=0, columnspan=2, pady=15)

    # Footer
    footer = tk.Label(container, text="© 2025 Hệ thống quản lý sinh viên", font=("Arial", 10), bg="#e0e0e0")
    footer.pack(side="bottom", fill="x")
