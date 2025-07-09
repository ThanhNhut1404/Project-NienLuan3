import tkinter as tk
from tkinter import messagebox
from Admin.Styles_admin import TITLE_FONT, LABEL_FONT, ENTRY_FONT, BUTTON_STYLE, CHECKBOX_STYLE

def render_admin_login(container):
    for widget in container.winfo_children():
        widget.destroy()

    content = tk.Frame(container, bg="#003366")
    content.pack(fill=tk.BOTH, expand=True)

    tk.Label(content, text="ĐĂNG NHẬP QUẢN TRỊ VIÊN", font=TITLE_FONT, bg="#003366", fg="white").pack(pady=20)

    # === Họ và tên ===
    tk.Label(content, text="Họ và tên:", font=LABEL_FONT, bg="#003366", fg="white").pack(anchor='w', padx=215)
    entry_name = tk.Entry(content, font=ENTRY_FONT, width=28)
    entry_name.pack(pady=(0, 15))

    # === Mật khẩu ===
    tk.Label(content, text="Mật khẩu:", font=LABEL_FONT, bg="#003366", fg="white").pack(anchor='w', padx=215)
    entry_password = tk.Entry(content, show="*", font=ENTRY_FONT, width=28)
    entry_password.pack(pady=(0, 10))

    # === Hiện mật khẩu (Checkbutton) ===
    show_password = tk.BooleanVar(value=False)

    def toggle_password():
        if show_password.get():
            entry_password.config(show="")  # Hiện
        else:
            entry_password.config(show="*")  # Ẩn

    tk.Checkbutton(
        content,
        text="Hiện mật khẩu",
        variable=show_password,
        command=toggle_password,
        **CHECKBOX_STYLE
    ).pack(anchor='w', padx=215, pady=(0, 15))

    # === Nút đăng nhập ===
    def handle_login():
        name = entry_name.get()
        password = entry_password.get()
        if name.lower() == "admin" and password == "123":
            from Admin.Admin_main import render_admin_main
            render_admin_main(container)
        else:
            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập.")

    tk.Button(content, text="Đăng nhập", command=handle_login, **BUTTON_STYLE).pack()
