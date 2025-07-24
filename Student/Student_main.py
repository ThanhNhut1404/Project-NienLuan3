import tkinter as tk
from tkinter import messagebox
import json
from Student.Styles_student import BUTTON_STYLE, MENU_BUTTON_STYLE
from Student.Header_student import render_header
from Student.Activity_roll_call import render_activity_roll_call
from Student.View_activity import render_view_activity
from Student.View_infor import render_view_infor
from Student.Update_sv import render_update_sv  # ✅ THÊM DÒNG NÀY

def render_student_main(container, user):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg="#f0f0f0")

    # ===== HEADER =====
    header_frame = tk.Frame(container, bg="#2C387E", height=55)
    header_frame.pack(fill="x")
    render_header(header_frame, user)

    # ===== MAIN CONTENT =====
    main_content = tk.Frame(container, bg="#f0f0f0")
    main_content.pack(fill="both", expand=True)

    # ===== NÚT MENU 3 GẠCH & KHUNG MENU =====
    menu_section = tk.Frame(main_content, bg="#f0f0f0")
    menu_section.pack(anchor="w", padx=20, pady=(10, 0))  # Sát bên trái

    menu_container = tk.Frame(container, bg="white", bd=2, relief="ridge")

    def show_info():
        render_view_infor(content_frame, user)
        menu_container.pack_forget()

    def show_view_activity():
        render_view_activity(content_frame, user)
        menu_container.pack_forget()

    def show_attendance():
        render_activity_roll_call(content_frame, user)
        menu_container.pack_forget()

    def show_update_info():
        render_update_sv(content_frame, user, go_back=lambda: render_student_main(container, user))
        menu_container.pack_forget()

    def logout():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            container.master.destroy()

    def toggle_menu():
        if menu_container.winfo_ismapped():
            menu_container.place_forget()
        else:
            x = menu_btn.winfo_rootx() - container.winfo_rootx()
            y = menu_btn.winfo_rooty() - container.winfo_rooty() + menu_btn.winfo_height()
            menu_container.place(x=x, y=y)

    menu_btn = tk.Button(
        menu_section,
        text="☰",
        font=("Arial", 18, "bold"),
        bg="#2C387E",
        fg="white",
        bd=0,
        padx=10,
        pady=5,
        command=toggle_menu
    )
    menu_btn.pack(anchor="w")  # Canh trái

    # ==== Thêm các nút chức năng vào menu_container ====
    tk.Button(menu_container, text="📅 Xem hoạt động đã tham gia", command=show_view_activity, **MENU_BUTTON_STYLE).pack(fill="x", pady=1)
    tk.Button(menu_container, text="📝 Điểm danh hoạt động", command=show_attendance, **MENU_BUTTON_STYLE).pack(fill="x", pady=1)
    tk.Button(menu_container, text="📝 Cập nhật thông tin", command=show_update_info, **MENU_BUTTON_STYLE).pack(fill="x",pady=1)
    tk.Button(menu_container, text="🚪 Đăng xuất", command=logout, **MENU_BUTTON_STYLE).pack(fill="x", pady=1)

    # ===== NỘI DUNG CHÍNH =====
    content_frame = tk.Frame(main_content, bg="white")  # Đã bỏ khung
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Hiển thị mặc định: Thông tin sinh viên
    render_view_infor(content_frame, user)
