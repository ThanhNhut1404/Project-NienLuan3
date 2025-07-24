import tkinter as tk
from tkinter import messagebox
from Student.Styles_student import MENU_BUTTON_STYLE
from Student.Activity_roll_call import render_activity_roll_call
from Student.View_activity import render_view_activity
from Student.Header_student import render_header
from Student.Update_sv import render_update_sv  # ✅ THÊM DÒNG NÀY

def render_student_main(container, user):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg="#f0f0f0")

    # ===== HEADER =====
    header_frame = tk.Frame(container, bg="#2C387E", height=60)
    header_frame.pack(fill="x")

    render_header(header_frame, user)

    # ===== NỘI DUNG CHÍNH =====
    main_content = tk.Frame(container, bg="#f0f0f0")
    main_content.pack(fill="both", expand=True)

    # ===== KHU VỰC HIỂN THỊ CHÍNH =====
    content_frame = tk.Frame(main_content, bg="white", bd=2, relief="groove")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ===== MENU ẨN (chỉ nằm trong main_content, không che header) =====
    menu_frame = tk.Frame(main_content, bg="white", bd=2, relief="ridge")

    def show_view_activity():
        menu_frame.place_forget()
        render_view_activity(content_frame, user)

    def show_attendance():
        menu_frame.place_forget()
        render_activity_roll_call(content_frame, user)

    def show_update_info():
        render_update_sv(content_frame, user)
        menu_frame.pack_forget()

    def logout():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            container.master.destroy()

    # ===== Các nút chức năng (với đường kẻ phân cách) =====
    tk.Button(menu_frame, text="📅 Hoạt động đã tham gia", command=show_view_activity, **MENU_BUTTON_STYLE).pack(fill="x", padx=10, pady=2)
    tk.Frame(menu_frame, height=1, bg="#ccc").pack(fill="x", padx=10, pady=1)

    tk.Button(menu_frame, text="📝 Điểm danh hoạt động", command=show_attendance, **MENU_BUTTON_STYLE).pack(fill="x", padx=10, pady=2)
    tk.Frame(menu_frame, height=1, bg="#ccc").pack(fill="x", padx=10, pady=1)

    tk.Button(menu_frame, text="📝 Cập nhật thông tin", command=show_update_info, **MENU_BUTTON_STYLE).pack(fill="x",pady=2)
    tk.Frame(menu_frame, height=1, bg="#ccc").pack(fill="x", padx=10, pady=1)

    tk.Button(menu_frame, text="🚪 Đăng xuất", command=logout, **MENU_BUTTON_STYLE).pack(fill="x", padx=10, pady=2)

    # ===== Nút menu ☰ đặt trong header (đè lên main_content) =====
    def toggle_menu():
        if menu_frame.winfo_ismapped():
            menu_frame.place_forget()
        else:
            menu_frame.place(x=10, y=10)

    menu_btn = tk.Button(
        header_frame,
        text="☰",
        font=("Arial", 20, "bold"),
        bg="#2C387E",
        fg="white",
        bd=0,
        activebackground="#1A237E",
        activeforeground="white",
        command=toggle_menu
    )
    menu_btn.place(x=10, y=10, width=40, height=40)

