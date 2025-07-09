# login.py
import tkinter as tk
from tkinter import messagebox
from database import get_all_users
from face_utils import capture_multiple_encodings, compare_face

def login_by_face():
    known_users = get_all_users()
    if not known_users:
        messagebox.showwarning("Chưa có dữ liệu", "Không có người dùng nào trong hệ thống.")
        return

    print("Đang so sánh khuôn mặt...")
    encodings = capture_multiple_encodings(num_captures=1)  # chỉ lấy 1 ảnh khi login
    if not encodings:
        messagebox.showerror("Lỗi", "Không thể nhận diện khuôn mặt.")
        return

    name, user_id = compare_face(encodings[0], known_users)
    if name:
        messagebox.showinfo("Thành công", f"Xin chào, {name} ({user_id})!")
    else:
        messagebox.showerror("Không thành công", "Không tìm thấy khuôn mặt trong hệ thống.")

root = tk.Tk()
root.title("Đăng nhập bằng khuôn mặt")

btn = tk.Button(root, text="Đăng nhập", command=login_by_face, font=("Arial", 14), width=20)
btn.pack(padx=20, pady=30)

root.mainloop()
