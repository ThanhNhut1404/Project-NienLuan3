import tkinter as tk
from tkinter import messagebox
from Admin.Styles_admin import (
    TITLE_FONT, LABEL_FONT, ENTRY_FONT, BUTTON_STYLE, CHECKBOX_STYLE,
    FORM_BG_COLOR, FORM_BORDER_WIDTH, FORM_BORDER_STYLE,
    FORM_PADDING_Y, FORM_LABEL_PADX, FORM_ENTRY_PADX,
    FORM_CHECKBOX_PADX, FORM_BUTTON_PADY
)

def render_admin_login(container):
    for widget in container.winfo_children():
        widget.destroy()

    content = tk.Frame(container, bg="#003366")
    content.pack(fill=tk.BOTH, expand=True)

    # === Tiêu đề ===
    tk.Label(content, text="ĐĂNG NHẬP QUẢN TRỊ VIÊN", font=TITLE_FONT, bg="#003366", fg="white").pack(pady=43)

    # === Form login (ô vuông) ===
    form_frame = tk.Frame(content, bg=FORM_BG_COLOR, bd=FORM_BORDER_WIDTH, relief=FORM_BORDER_STYLE)
    form_frame.config(width=500, height=350)
    form_frame.place(relx=0.5, rely=0.4, anchor="center")  # Canh giữa màn hình

    # === Họ và tên ===
    tk.Label(form_frame, text="Họ và tên:", font=LABEL_FONT, bg=FORM_BG_COLOR, fg="black")\
        .pack(anchor='w', padx=FORM_LABEL_PADX, pady=(FORM_PADDING_Y, 5))
    entry_name = tk.Entry(form_frame, font=ENTRY_FONT, width=30)
    entry_name.pack(padx=FORM_ENTRY_PADX)

    # === Mật khẩu ===
    tk.Label(form_frame, text="Mật khẩu:", font=LABEL_FONT, bg=FORM_BG_COLOR, fg="black")\
        .pack(anchor='w', padx=FORM_LABEL_PADX, pady=(15, 5))
    entry_password = tk.Entry(form_frame, show="*", font=ENTRY_FONT, width=30)
    entry_password.pack(padx=FORM_ENTRY_PADX)

    # === Checkbutton hiện mật khẩu ===
    show_password = tk.BooleanVar(value=False)

    def toggle_password():
        entry_password.config(show="" if show_password.get() else "*")

    tk.Checkbutton(
        form_frame,
        text="Hiện mật khẩu",
        variable=show_password,
        command=toggle_password,
        **CHECKBOX_STYLE
    ).pack(anchor='w', padx=FORM_CHECKBOX_PADX, pady=(10, 10))

    # === Nút đăng nhập ===
    def handle_login():
        name = entry_name.get()
        password = entry_password.get()
        if name.lower() == "admin" and password == "123":
            from Admin.Admin_main import render_admin_main
            render_admin_main(container)
        else:
            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập.")

    tk.Button(form_frame, text="Đăng Nhập", command=handle_login, **BUTTON_STYLE)\
        .pack(pady=(0, FORM_BUTTON_PADY))
