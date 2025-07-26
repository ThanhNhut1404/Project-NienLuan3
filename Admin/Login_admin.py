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

    content = tk.Frame(container, bg="white")
    content.pack(fill=tk.BOTH, expand=True)

    tk.Label(content, text="ĐĂNG NHẬP QUẢN TRỊ VIÊN", font=("Arial", 20, "bold"), bg="white", fg="#003366") \
        .pack(pady=65, anchor="w", fill="x", padx=20)

    # === Form login (ô vuông) ===
    form_frame = tk.Frame(content, bg=FORM_BG_COLOR, bd=FORM_BORDER_WIDTH, relief=FORM_BORDER_STYLE)
    form_frame.config(width=600, height=500)
    form_frame.place(relx=0.5, rely=0.3, anchor="center")  # Canh giữa màn hình

    # === Họ và tên ===
    name_row = tk.Frame(form_frame, bg=FORM_BG_COLOR)
    name_row.pack(pady=(FORM_PADDING_Y, 0), padx=FORM_ENTRY_PADX, anchor="w")
    tk.Label(name_row, text="Họ và tên:", font=LABEL_FONT, bg=FORM_BG_COLOR, fg="white", width=9, anchor="w").pack(
        side="left")
    entry_name = tk.Entry(name_row, font=ENTRY_FONT, width=22)
    entry_name.pack(side="left", padx=FORM_ENTRY_PADX)

    # === Mật khẩu ===
    pass_row = tk.Frame(form_frame, bg=FORM_BG_COLOR)
    pass_row.pack(pady=(8, 0), padx=FORM_ENTRY_PADX, anchor="w")
    tk.Label(pass_row, text="Mật khẩu:", font=LABEL_FONT, bg=FORM_BG_COLOR, fg="white", width=9, anchor="w").pack(
        side="left")
    entry_password = tk.Entry(pass_row, show="*", font=ENTRY_FONT, width=22)
    entry_password.pack(side="left", padx=FORM_ENTRY_PADX)

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
