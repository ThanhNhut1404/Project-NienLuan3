import tkinter as tk
from tkinter import messagebox
import json
from Student.Styles_student import *
from Student.Header_student import render_header
from Student.View_infor import render_view_infor
from Student.Menu_student import render_menu
from Student.Dashboard import render_dashboard
from Student.Chart_activity import render_chart_activity

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

    # ===== MENU BUTTON =====
    menu_btn = tk.Button(
        container,
        text="☰",
        font=("Arial", 18, "bold"),
        bg="#00897B",
        fg="white",
        bd="2",
        relief="raised",
        activebackground="#00897B",
        activeforeground="white"
    )
    menu_btn.place(x=10, y=60, width=40, height=40)  # nằm dưới header

    # ===== MENU =====
    render_menu(container, content_frame, user, menu_btn, go_back_login=lambda: open_student_login(container))

    # ===== HIỂN THỊ MẶC ĐỊNH =====
    render_dashboard(content_frame, user)


# ===== DASHBOARD (thông tin + biểu đồ) =====
def render_dashboard(content_frame, user):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # ===== HIỂN THỊ THÔNG TIN SINH VIÊN =====
    render_view_infor(content_frame, user)
 # ===== KHUNG CHỨA BIỂU ĐỒ =====
    chart_frame = tk.Frame(content_frame, bg="#f0f0f0")
    chart_frame.pack(fill="x", pady=(10, 20))

    # ===== HIỂN THỊ BIỂU ĐỒ =====
    render_chart_activity(chart_frame, user, title="📊 Tiến độ điểm rèn luyện học kỳ hiện tại")