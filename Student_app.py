import tkinter as tk
from Student.Login_student import open_student_login
from Student.Styles_student import APP_SIZE

def start_student_app():
    # Tạo cửa sổ chính cho sinh viên
    root = tk.Tk()
    root.title("Hệ thống điểm danh - Sinh viên")
    root.geometry(APP_SIZE)
    root.configure(bg="white")
    root.resizable(False, False)

    # Vùng container để render nội dung
    container = tk.Frame(root, bg="white")
    container.pack(fill="both", expand=True)

    # Gọi giao diện đăng nhập sinh viên
    open_student_login(container)

    root.mainloop()

if __name__ == "__main__":
    start_student_app()
