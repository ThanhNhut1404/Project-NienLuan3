import tkinter as tk
from Admin.Styles_admin import TITLE_FONT
from Admin.Header_admin import render_header
from PIL import Image, ImageTk
import os


def render_admin_main(container):
    from Admin.Login_admin import render_admin_login  # tránh import vòng lặp

    # Xóa toàn bộ nội dung cũ
    for widget in container.winfo_children():
        widget.destroy()

    # === Biến lưu hàm dọn dẹp của view hiện tại (nếu có) ===
    current_cleanup = {"func": None}

    # === Hàm chuyển view ===
    def switch_to_view(view_name):
        # Gọi hàm dọn dẹp hiện tại nếu có (ví dụ: tắt camera)
        if current_cleanup["func"]:
            try:
                current_cleanup["func"]()
            except Exception as e:
                print("[Lỗi dọn dẹp view]:", e)
            current_cleanup["func"] = None

        for widget in main_content.winfo_children():
            widget.destroy()

        if view_name == "create_student":
            from Admin.Create_student import render_student_create
            current_cleanup["func"] = render_student_create(main_content, switch_to_view)
        elif view_name == "view_students":
            from Admin.List_student import render_student_list
            render_student_list(main_content, go_back=switch_to_view)
        elif view_name == "create_activity":
            from Admin.Create_activity import render_Create_activity
            render_Create_activity(main_content)
        elif view_name == "view_activities":
            from Admin.List_view_activity import render_list_view_activity
            render_list_view_activity(main_content, switch_to_view)
        elif view_name == "create_hk":
            from Admin.Create_HK import render_create_hoc_ky
            render_create_hoc_ky(main_content)
        elif view_name == "list_view_hk":
            from Admin.List_view_HK import render_list_view_hk
            render_list_view_hk(main_content, go_back=switch_to_view)

        else:
            render_dashboard()

    # Đường dẫn đến ảnh tiêu đề
    title_image_path = os.path.join("Image", "banner_top.jpg")  # đổi tên nếu cần

    # Mở và resize ảnh: ví dụ chiều cao 100px (banner ngang)
    title_img = Image.open(title_image_path)
    title_img = title_img.resize((982, 45), Image.Resampling.LANCZOS)  # hoặc tuỳ theo kích thước frame
    title_photo = ImageTk.PhotoImage(title_img)

    # Gắn ảnh vào label
    title_img_label = tk.Label(container, image=title_photo, bg="white")
    title_img_label.image = title_photo  # giữ tham chiếu ảnh
    title_img_label.pack(side=tk.TOP, fill=tk.X)

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

        # Đường dẫn đến ảnh
        image_path = os.path.join("Image", "banner_admin.jpg")

        # Mở và resize ảnh cho vừa vùng nội dung
        img = Image.open(image_path)
        img = img.resize((979, 550), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        # Tạo label chứa ảnh
        img_label = tk.Label(main_content, image=photo, bg="white")
        img_label.image = photo  # Lưu tham chiếu ảnh tránh bị xóa
        img_label.pack(pady=30)

    # Gọi dashboard mặc định
    render_dashboard()
