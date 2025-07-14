import tkinter as tk
from Admin.Styles_admin import TITLE_FONT
from Admin.Header_admin import render_header

def render_admin_main(container):
    from Admin.Login_admin import render_admin_login  # tránh import vòng lặp

    # Xóa toàn bộ nội dung cũ
    for widget in container.winfo_children():
        widget.destroy()

    # === Hàm chuyển view ===
    def switch_to_view(view_name):
        for widget in main_content.winfo_children():
            widget.destroy()

        if view_name == "create_student":
            from Admin.Create_student import render_student_create
            render_student_create(main_content, switch_to_view)
        elif view_name == "view_students":
            from Admin.List_student import render_student_list
            render_student_list(main_content)
        elif view_name == "create_activity":
            tk.Label(main_content, text="📌 Tạo hoạt động", font=TITLE_FONT, bg="white").pack(pady=40)
        elif view_name == "view_activities":
            tk.Label(main_content, text="📅 Danh sách hoạt động", font=TITLE_FONT, bg="white").pack(pady=40)
        else:
            render_dashboard()

    # === Tiêu đề hệ thống luôn nằm trên cùng ===
    title_label = tk.Label(
        container,
        text="🎓 HỆ THỐNG ĐIỂM DANH SINH VIÊN - ADMIN",
        font=TITLE_FONT,
        fg="#2E4053",
        bg="white",
        pady=10
    )
    title_label.pack(side=tk.TOP, fill=tk.X)

    # === Gọi header ngay dưới tiêu đề ===
    header = render_header(
        container,
        on_logout=lambda: render_admin_login(container),
        switch_to_view=switch_to_view
    )
    header.pack(side=tk.TOP, fill=tk.X)

    # === Vùng nội dung bên dưới menu ===
    global main_content
    main_content = tk.Frame(container, bg="white")
    main_content.pack(fill=tk.BOTH, expand=True)

    # === Trang mặc định dashboard ===
    def render_dashboard():
        for widget in main_content.winfo_children():
            widget.destroy()
        tk.Label(
            main_content,
            text="📊 Tổng quan hệ thống",
            font=TITLE_FONT,
            fg="#2E4053",
            bg="white"
        ).pack(pady=40)

    # Gọi dashboard mặc định
    render_dashboard()
