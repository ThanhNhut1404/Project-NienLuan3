import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from Student.Styles_student import LABEL_FONT, ENTRY_FONT, BUTTON_STYLE

def open_student_login(container):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg="white")
    cap = cv2.VideoCapture(0)

    # ==== Camera bên trái (Frame + Label để đồng bộ bên phải) ====
    left_frame = tk.Frame(container, bg="white", bd=2, relief="groove")
    left_frame.place(relx=0.02, rely=0.05, relwidth=0.45, relheight=0.9)

    title_cam = tk.Label(
        left_frame,
        text="CAMERA NHẬN DIỆN KHUÔN MẶT",
        font=("Arial", 14, "bold"),
        bg="white"
    )
    title_cam.pack(pady=(15, 5))

    cam_label = tk.Label(left_frame, bg="white")
    cam_label.pack()

    def update_camera():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (360, 270))
            frame = cv2.flip(frame, 1)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            cam_label.imgtk = imgtk
            cam_label.configure(image=imgtk)
        cam_label.after(10, update_camera)

    update_camera()

    # ==== Form bên phải (đồng bộ khung) ====
    right_frame = tk.Frame(container, bg="white", bd=2, relief="groove")
    right_frame.place(relx=0.52, rely=0.05, relwidth=0.45, relheight=0.9)

    title_label = tk.Label(
        right_frame,
        text="ĐĂNG NHẬP SINH VIÊN",
        font=("Arial", 14, "bold"),
        bg="white"
    )
    title_label.pack(pady=(15, 5))

    form_container = tk.Frame(right_frame, bg="white")
    form_container.pack(anchor='n', pady=(5, 0))  # Dịch lên gần đầu

    tk.Label(form_container, text="Họ và tên:", font=LABEL_FONT, bg="white").pack(anchor='w', pady=(0, 6))
    entry_name = tk.Entry(form_container, width=36, font=ENTRY_FONT)
    entry_name.pack(pady=(0, 18))

    tk.Label(form_container, text="Mã số sinh viên:", font=LABEL_FONT, bg="white").pack(anchor='w', pady=(0, 6))
    entry_mssv = tk.Entry(form_container, width=36, font=ENTRY_FONT)
    entry_mssv.pack(pady=(0, 18))

    tk.Label(form_container, text="Mật khẩu:", font=LABEL_FONT, bg="white").pack(anchor='w', pady=(0, 6))
    entry_password = tk.Entry(form_container, show="*", width=36, font=ENTRY_FONT)
    entry_password.pack(pady=(0, 22))

    def student_login():
        name = entry_name.get()
        mssv = entry_mssv.get()
        password = entry_password.get()
        messagebox.showinfo("Đăng nhập", f"Đang kiểm tra thông tin cho {name} - {mssv}")
        # TODO: xác thực CSDL
        # cap.release()
        # from Student.Student_main import render_student_main
        # render_student_main(container)

    tk.Button(form_container, text="Đăng nhập", command=student_login, **BUTTON_STYLE).pack(pady=12)

    # Đóng app → release camera
    container.winfo_toplevel().protocol("WM_DELETE_WINDOW", lambda: (cap.release(), container.winfo_toplevel().destroy()))
