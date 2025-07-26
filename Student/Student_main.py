import tkinter as tk
from tkinter import messagebox
import json
from Student.Styles_student import *
from Student.Header_student import render_header
from Student.View_infor import render_view_infor
from Student.Menu_student import render_menu


def render_student_main(container, user):
    from Student.Login_student import open_student_login
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg="#f0f0f0")

    # ===== HEADER =====
    header_frame = tk.Frame(container, bg="#00897B", height=45)
    header_frame.pack(fill="x")
    render_header(header_frame, user)

    # ===== MAIN CONTENT =====
    main_content = tk.Frame(container, bg="#f0f0f0")
    main_content.pack(fill="both", expand=True)

    # ===== NỘI DUNG CHÍNH =====
    content_frame = main_content

    # ===== NÚT MENU ☰ (bên dưới header, nhưng nằm đè lên toàn bộ) =====
    menu_btn = tk.Button(
        container,
        text="☰",
        font=("Arial", 20, "bold"),
        bg="#00897B",
        fg="white",
        bd = "2",
        relief= "raised",
        activebackground="#00897B",
        activeforeground="white"
    )
    menu_btn.place(x=10, y=60, width=40, height=40)  # Y=60 để nằm dưới header (height=55)

    # ===== GỌI MENU RIÊNG (menu_btn truyền vào để định vị menu_frame) =====
    render_menu(container, content_frame, user, menu_btn, go_back_login=lambda: open_student_login(container))

    # ===== HIỂN THỊ MẶC ĐỊNH =====
    render_view_infor(content_frame, user)
