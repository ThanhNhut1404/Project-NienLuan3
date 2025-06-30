import tkinter as tk
from Student.Login_student import open_student_login  # Import trong cùng thư mục

def start_student_app():
    root = tk.Tk()
    root.title("Hệ thống điểm danh - Sinh viên")
    root.geometry("400x200")

    tk.Label(root, text="SINH VIÊN", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Đăng nhập", width=20, command=lambda: open_student_login(root)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_student_app()
