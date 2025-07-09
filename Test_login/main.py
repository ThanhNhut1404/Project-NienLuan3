# main.py
import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os
import sys
import sqlite3
from database import init_db

# Khởi tạo DB khi chạy lần đầu
init_db()

# Hàm chạy file con bằng đúng Python đang chạy main.py
def run_script(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    subprocess.Popen([sys.executable, path])  # DÙNG sys.executable để tránh lỗi môi trường

# Hàm xóa người dùng theo ID
def delete_user():
    user_id = simpledialog.askstring("Xóa người dùng", "Nhập ID cần xóa:")
    if user_id:
        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            deleted = c.rowcount
            conn.commit()
            conn.close()
            if deleted:
                messagebox.showinfo("Xóa thành công", f"Đã xóa {deleted} dòng cho ID {user_id}")
            else:
                messagebox.showwarning("Không tìm thấy", f"Không có dữ liệu nào với ID {user_id}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

# Giao diện chính
root = tk.Tk()
root.title("HỆ THỐNG ĐĂNG NHẬP BẰNG KHUÔN MẶT")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="CHỌN CHỨC NĂNG", font=("Arial", 16, "bold")).pack(pady=20)

btn_register = tk.Button(root, text="Đăng ký khuôn mặt", font=("Arial", 12), width=30,
                         command=lambda: run_script("register.py"))
btn_register.pack(pady=10)

btn_login = tk.Button(root, text="Đăng nhập bằng khuôn mặt", font=("Arial", 12), width=30,
                      command=lambda: run_script("login.py"))
btn_login.pack(pady=10)

btn_delete = tk.Button(root, text="Xóa người dùng theo ID", font=("Arial", 12), width=30,
                       command=delete_user)
btn_delete.pack(pady=10)

root.mainloop()
