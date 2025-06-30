import tkinter as tk
from tkinter import messagebox

def open_admin_login(parent_root):
    login_window = tk.Toplevel(parent_root)
    login_window.title("Đăng nhập quản trị viên")
    login_window.geometry("400x300")

    tk.Label(login_window, text="Đăng nhập Quản trị viên", font=("Arial", 14)).pack(pady=10)

    tk.Label(login_window, text="Tài khoản:").pack(anchor='w', padx=20)
    entry_username = tk.Entry(login_window)
    entry_username.pack(padx=20)

    tk.Label(login_window, text="Mật khẩu:").pack(anchor='w', padx=20)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(padx=20)

    def admin_login():
        name = entry_name.get()
        username = entry_username.get()
        password = entry_password.get()
        if username == "admin" and password == "123":
            messagebox.showinfo("Đăng nhập thành công", f"Chào quản trị viên {name}")
        else:
            messagebox.showerror("Thất bại", "Sai tài khoản hoặc mật khẩu")

    tk.Button(login_window, text="Đăng nhập", command=admin_login).pack(pady=15)
