import tkinter as tk
from Admin.Styles_admin import MENU_BUTTON_STYLE, SEPARATOR_STYLE
from PIL import Image, ImageTk
import os


def render_header(container, on_logout, switch_to_view):
    header = tk.Frame(container, bg="#003366", height=50)

    # === Nút Home (Trang chính) ===
    home_icon_path = os.path.join("Image", "home_icon.png")
    home_img = Image.open(home_icon_path)
    home_img = home_img.resize((20, 20), Image.Resampling.LANCZOS)
    home_photo = ImageTk.PhotoImage(home_img)

    home_btn = tk.Button(
        header,
        image=home_photo,
        bg="#003366",
        activebackground="#003366",
        bd=0,
        command=lambda: switch_to_view(None)  # gọi trang chính (dashboard)
    )
    home_btn.image = home_photo  # giữ tham chiếu ảnh
    home_btn.pack(side=tk.LEFT, padx=10)


    # === MENU: Quản lý sinh viên ===
    student_menu_btn = tk.Menubutton(header, text="Quản lý sinh viên", **MENU_BUTTON_STYLE, direction="below")
    student_menu = tk.Menu(student_menu_btn, tearoff=0, font=("Arial", 10), fg="#003366")
    student_menu.add_command(label="Tạo tài khoản sinh viên", command=lambda: switch_to_view("create_student"))
    student_menu.add_separator()
    student_menu.add_command(label="Xem danh sách sinh viên", command=lambda: switch_to_view("view_students"))
    student_menu.add_separator()
    student_menu_btn.config(menu=student_menu)
    student_menu_btn.pack(side=tk.LEFT, padx=2)

    # === Phân cách dọc giữa menu lớn ===
    separator1 = tk.Frame(header, **SEPARATOR_STYLE)
    separator1.pack(side=tk.LEFT, padx=5, pady=10)

    # === MENU: Quản lý hoạt động ===
    activity_menu_btn = tk.Menubutton(header, text="Quản lý hoạt động", **MENU_BUTTON_STYLE, direction="below")
    activity_menu = tk.Menu(activity_menu_btn, tearoff=0, font=("Arial", 10), fg="#003366")
    activity_menu.add_command(label="Tạo hoạt động", command=lambda: switch_to_view("create_activity"))
    activity_menu.add_separator()
    activity_menu.add_command(label="Xem danh sách hoạt động", command=lambda: switch_to_view("view_activities"))
    activity_menu.add_separator()
    activity_menu_btn.config(menu=activity_menu)
    activity_menu_btn.pack(side=tk.LEFT, padx=2)

    # === Phân cách dọc giữa menu lớn ===
    separator2 = tk.Frame(header, **SEPARATOR_STYLE)
    separator2.pack(side=tk.LEFT, padx=5, pady=10)

    # === MENU: Quản lý học kỳ ===
    semester_menu_btn = tk.Menubutton(header, text="Quản lý học kỳ", **MENU_BUTTON_STYLE, direction="below")
    semester_menu = tk.Menu(semester_menu_btn, tearoff=0, font=("Arial", 10), fg="#003366")
    semester_menu.add_command(label="Tạo học kỳ", command=lambda: switch_to_view("create_hk"))
    semester_menu.add_separator()
    semester_menu.add_command(label="Xem danh sách học kỳ", command=lambda: switch_to_view("list_view_hk"))
    semester_menu.add_separator()
    semester_menu_btn.config(menu=semester_menu)
    semester_menu_btn.pack(side=tk.LEFT, padx=2)

    # === Phân cách dọc giữa menu lớn ===
    separator2 = tk.Frame(header, **SEPARATOR_STYLE)
    separator2.pack(side=tk.LEFT, padx=5, pady=10)

    # === MENU: Quản lý thống kê ===
    stats_menu_btn = tk.Menubutton(header, text="Quản lý thống kê", **MENU_BUTTON_STYLE, direction="below")
    stats_menu = tk.Menu(stats_menu_btn, tearoff=0, font=("Arial", 10), fg="#003366")
    stats_menu.add_command(label="Thống kê điểm danh", command=lambda: switch_to_view("view_statistics"))
    stats_menu.add_separator()
    stats_menu_btn.config(menu=stats_menu)
    stats_menu_btn.pack(side=tk.LEFT, padx=2)

    # === Phân cách dọc ===
    separator3 = tk.Frame(header, **SEPARATOR_STYLE)
    separator3.pack(side=tk.LEFT, padx=5, pady=10)

    # === MENU: Quản lý tài khoản ===
    account_menu_btn = tk.Menubutton(header, text="Quản lý tài khoản", **MENU_BUTTON_STYLE, direction="below")
    account_menu = tk.Menu(account_menu_btn, tearoff=0, font=("Arial", 10), fg="#003366")
    account_menu.add_command(label="Tạo tài khoản admin", command=lambda: switch_to_view("create_admin"))
    account_menu.add_separator()
    account_menu.add_command(label="Danh sách tài khoản", command=lambda: switch_to_view("view_admins"))
    account_menu.add_separator()
    account_menu_btn.config(menu=account_menu)
    account_menu_btn.pack(side=tk.LEFT, padx=2)


    # === Nút logout icon (bên phải) ===
    logout_icon_path = os.path.join("Image", "logout_icon.png")
    logout_img = Image.open(logout_icon_path)
    logout_img = logout_img.resize((27, 27), Image.Resampling.LANCZOS)
    logout_photo = ImageTk.PhotoImage(logout_img)

    logout_btn = tk.Button(
        header,
        image=logout_photo,
        bg="#003366",
        activebackground="#003366",
        bd=0,
        command=on_logout
    )
    logout_btn.image = logout_photo  # giữ tham chiếu ảnh
    logout_btn.pack(side=tk.RIGHT, padx=10)

    return header  # Trả về để .pack() ở ngoài
