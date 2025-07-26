import tkinter as tk
from tkinter import messagebox
from Student.Styles_student import MENU_BUTTON_STYLE
from Student.Activity_roll_call import render_activity_roll_call
from Student.View_activity import render_view_activity
from Student.Update_sv import render_update_sv
from Student.View_infor import render_view_infor

def render_menu(container, content_frame, user, menu_btn, go_back_login):
    menu_frame = tk.Frame(container, bg="white", bd=2, relief="ridge")

    def show_home():
        menu_frame.place_forget()
        render_view_infor(content_frame, user)

    def show_view_activity():
        menu_frame.place_forget()
        render_view_activity(content_frame, user)

    def show_attendance():
        menu_frame.place_forget()
        render_activity_roll_call(content_frame, user)

    def show_update_info():
        menu_frame.place_forget()
        render_update_sv(content_frame, user, show_home)

    def logout():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            menu_frame.place_forget()
            go_back_login()

    # ===== NÚT MENU ☰ ĐIỀU KHIỂN MENU =====
    def toggle_menu():
        if menu_frame.winfo_ismapped():
            menu_frame.place_forget()
        else:
            x = menu_btn.winfo_rootx() - container.winfo_rootx()
            y = menu_btn.winfo_rooty() - container.winfo_rooty() + menu_btn.winfo_height()
            menu_frame.place(x=x, y=y)

    menu_btn.config(command=toggle_menu)

    # ===== CÁC NÚT TRONG MENU =====
    tk.Button(menu_frame, text="Trang chủ", command=show_home, **MENU_BUTTON_STYLE).pack(fill="x", padx=10, pady=2)
    tk.Frame(menu_frame, height=1, bg="#ccc").pack(fill="x", padx=10, pady=1)

    tk.Button(menu_frame, text="Hoạt động đã tham gia", command=show_view_activity, **MENU_BUTTON_STYLE).pack(fill="x", padx=10, pady=2)
    tk.Frame(menu_frame, height=1, bg="#ccc").pack(fill="x", padx=10, pady=1)

    tk.Button(menu_frame, text="Điểm danh hoạt động", command=show_attendance, **MENU_BUTTON_STYLE).pack(fill="x", padx=10, pady=2)
    tk.Frame(menu_frame, height=1, bg="#ccc").pack(fill="x", padx=10, pady=1)

    tk.Button(menu_frame, text="Cập nhật thông tin", command=show_update_info, **MENU_BUTTON_STYLE).pack(fill="x", padx=10, pady=2)
    tk.Frame(menu_frame, height=1, bg="#ccc").pack(fill="x", padx=10, pady=1)

    tk.Button(menu_frame, text="Đăng xuất", command=logout, **MENU_BUTTON_STYLE).pack(fill="x", padx=10, pady=2)
