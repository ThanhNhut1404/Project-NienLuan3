import tkinter as tk
from Admin.Login_admin import open_admin_login  # Import trong cùng thư mục

def start_admin_app():
    root = tk.Tk()
    root.title("Hệ thống điểm danh - Admin")
    root.geometry("400x200")

    tk.Label(root, text="QUẢN TRỊ VIÊN", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Đăng nhập", width=20, command=lambda: open_admin_login(root)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_admin_app()
