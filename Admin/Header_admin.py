import tkinter as tk
from Admin.Styles_admin import MENU_BUTTON_STYLE, SEPARATOR_STYLE

def render_header(container, on_logout, switch_to_view):
    header = tk.Frame(container, bg="#003366", height=50)

    # === MENU: Quản lý sinh viên ===
    student_menu_btn = tk.Menubutton(header, text="Quản lý sinh viên", **MENU_BUTTON_STYLE, direction="below")
    student_menu = tk.Menu(student_menu_btn, tearoff=0, font=("Arial", 10), fg="#003366")
    student_menu.add_command(label="Tạo tài khoản", command=lambda: switch_to_view("create_student"))
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

    # === Nút Đăng xuất (nằm bên phải) ===
    tk.Button(header, text="Đăng xuất", command=on_logout, **MENU_BUTTON_STYLE).pack(side=tk.RIGHT, padx=10)

    return header  # Trả về để .pack() ở ngoài
