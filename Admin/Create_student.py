import tkinter as tk
from Admin.Styles_admin import TITLE_FONT, LABEL_FONT, ENTRY_FONT, BUTTON_STYLE

def render_create_student(container):
    for widget in container.winfo_children():
        widget.destroy()

    content = tk.Frame(container, bg="white")
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    tk.Label(content, text="📌 Tạo tài khoản sinh viên", font=TITLE_FONT, bg="white").pack(pady=(0, 20))

    tk.Label(content, text="Họ và tên:", font=LABEL_FONT, bg="white").pack(anchor="w")
    entry_name = tk.Entry(content, font=ENTRY_FONT, width=35)
    entry_name.pack(pady=(0, 15))

    tk.Label(content, text="Mã số sinh viên:", font=LABEL_FONT, bg="white").pack(anchor="w")
    entry_mssv = tk.Entry(content, font=ENTRY_FONT, width=35)
    entry_mssv.pack(pady=(0, 15))

    tk.Label(content, text="Mật khẩu:", font=LABEL_FONT, bg="white").pack(anchor="w")
    entry_password = tk.Entry(content, show="*", font=ENTRY_FONT, width=35)
    entry_password.pack(pady=(0, 20))

    def handle_create():
        print("✔ Đã tạo:", entry_name.get(), entry_mssv.get(), entry_password.get())

    tk.Button(content, text="Tạo tài khoản", command=handle_create, **BUTTON_STYLE).pack()
