import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

def open_student_login(parent_root):
    login_window = tk.Toplevel(parent_root)
    login_window.title("Đăng nhập sinh viên")
    login_window.geometry("800x400")

    # Form đăng nhập bên trái
    left_frame = tk.Frame(login_window)
    left_frame.pack(side=tk.LEFT, padx=20, pady=20)

    tk.Label(left_frame, text="Họ và tên:").pack(anchor='w')
    entry_name = tk.Entry(left_frame)
    entry_name.pack()

    tk.Label(left_frame, text="MSSV:").pack(anchor='w')
    entry_mssv = tk.Entry(left_frame)
    entry_mssv.pack()

    tk.Label(left_frame, text="Mật khẩu:").pack(anchor='w')
    entry_password = tk.Entry(left_frame, show="*")
    entry_password.pack()

    def student_login():
        name = entry_name.get()
        mssv = entry_mssv.get()
        password = entry_password.get()
        messagebox.showinfo("Đăng nhập", f"Đang kiểm tra thông tin cho {name} - {mssv}")
        # TODO: xác thực với cơ sở dữ liệu

    tk.Button(left_frame, text="Đăng nhập", command=student_login).pack(pady=10)

    # Khung mở camera bên phải
    right_frame = tk.Frame(login_window)
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

    cam_label = tk.Label(right_frame)
    cam_label.pack()

    cap = cv2.VideoCapture(0)

    def update_camera():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            cam_label.imgtk = imgtk
            cam_label.configure(image=imgtk)
        cam_label.after(10, update_camera)

    update_camera()

    def on_close():
        cap.release()
        login_window.destroy()

    login_window.protocol("WM_DELETE_WINDOW", on_close)
