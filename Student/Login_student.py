import tkinter as tk
from tkinter import messagebox
import json
import cv2
import face_recognition
import numpy as np
import hashlib
from PIL import Image, ImageTk

from Database.Create_db import get_all_sinh_vien
from Student.Student_main import render_student_main
from Student.Styles_student import LABEL_FONT, ENTRY_FONT, BUTTON_STYLE


def open_student_login(container):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg="white")

    cap = cv2.VideoCapture(0)
    current_frame = {'image': None}

    # ====== TIÊU ĐỀ CHÍNH TRÊN CÙNG ====== #
    title_label = tk.Label(
        container,
        text="CỔNG ĐĂNG NHẬP SINH VIÊN",
        font=("Helvetica", 22, "bold"),
        bg="white",
        fg="#002244"
    )
    title_label.place(relx=0.5, rely=0.01, anchor="n")  # Canh giữa theo chiều ngang

    # ====== FRAME CAMERA (có viền) ====== #
    camera_frame = tk.Frame(container, bg="white", bd=2, relief="groove")
    camera_frame.place(relx=0.05, rely=0.1, relwidth=0.42, relheight=0.80)

    tk.Label(
        camera_frame,
        text="ĐĂNG NHẬP BẰNG KHUÔN MẶT",
        font=("Arial", 16, "bold"),
        bg="white", fg="#003366"
    ).pack(pady=(10, 5))
    note_label = tk.Label(
        camera_frame,
        text="Nếu không muốn đăng nhập bằng tài khoản,\n bạn có thể dùng khuôn mặt để đăng nhập.",
        font=("Arial", 10, "italic"),
        fg="red",
        bg="white",
        justify="center"
    )
    note_label.pack(pady=(0, 10))

    cam_label = tk.Label(camera_frame, bg="white")
    cam_label.pack(pady=10, padx=10, expand=True)


    def update_camera():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (400, 300))
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            current_frame['image'] = rgb_frame
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            cam_label.imgtk = imgtk
            cam_label.configure(image=imgtk)
        cam_label.after(10, update_camera)

    update_camera()

    tk.Button(
        camera_frame,
        text="🔓 Đăng nhập",
        command=lambda: face_login(current_frame, cap, container),
        **BUTTON_STYLE
    ).pack(pady=(10, 20))

    # ====== FORM ĐĂNG NHẬP BẰNG MSSV (có viền) ====== #
    right_frame = tk.Frame(container, bg="#E0F2F1", bd=2, relief="groove")
    right_frame.place(relx=0.52, rely=0.1, relwidth=0.43, relheight=0.80)

    tk.Label(
        right_frame,
        text="ĐĂNG NHẬP BẰNG TÀI KHOẢN",
        font=("Arial", 16, "bold"),
        bg="#E0F2F1", fg="#003366"
    ).pack(pady=(30, 20))

    form_frame = tk.Frame(right_frame, bg="#E0F2F1")
    form_frame.pack()

    tk.Label(form_frame, text="MSSV:", font=LABEL_FONT, bg="#E0F2F1", fg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    mssv_entry = tk.Entry(form_frame, font=ENTRY_FONT, width=30)
    mssv_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Mật khẩu:", font=LABEL_FONT, bg="#E0F2F1").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    password_entry = tk.Entry(form_frame, show="*", font=ENTRY_FONT, width=30)
    password_entry.grid(row=1, column=1, pady=5)

    def login_by_account():
        mssv = mssv_entry.get().strip()
        raw_password = password_entry.get().strip()

        if not mssv or not raw_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ MSSV và mật khẩu.")
            return

        password = hashlib.sha256(raw_password.encode()).hexdigest()

        all_users = get_all_sinh_vien()
        for user in all_users:
            if user["mssv"] == mssv and user.get("password") == password:
                cap.release()
                render_student_main(container, user)
                return

        messagebox.showerror("Lỗi", "Sai MSSV hoặc mật khẩu.")

    tk.Button(
        right_frame,
        text="🔓 Đăng nhập",
        command=login_by_account,
        **BUTTON_STYLE
    ).pack(pady=(30, 10))

    # ======= ĐÓNG ỨNG DỤNG ======= #
    container.winfo_toplevel().protocol(
        "WM_DELETE_WINDOW",
        lambda: (cap.release(), container.winfo_toplevel().destroy())
    )



def face_login(frame_dict, cap, container):
    img = frame_dict.get('image')
    if img is None:
        messagebox.showerror("Lỗi", "Chưa có khung hình từ camera.")
        return

    boxes = face_recognition.face_locations(img)
    if len(boxes) != 1:
        messagebox.showerror("Lỗi", "Vui lòng đảm bảo chỉ có 1 khuôn mặt trước camera.")
        return

    unknown_encoding = face_recognition.face_encodings(img, boxes)[0]
    all_users = get_all_sinh_vien()
    if not all_users:
        messagebox.showwarning("Không có dữ liệu", "Không tìm thấy người dùng trong hệ thống.")
        return

    for user in all_users:
        enc_list = user.get("encodings", [])
        if not enc_list:
            continue

        for known_encoding in enc_list:
            try:
                if isinstance(known_encoding, str):
                    known_encoding = json.loads(known_encoding)
                known_np = np.array(known_encoding, dtype=np.float64)
                match = face_recognition.compare_faces([known_np], unknown_encoding, tolerance=0.40)[0]
                if match:
                    cap.release()
                    render_student_main(container, user)
                    return
            except Exception as e:
                print("[Lỗi] So sánh encoding:", e)
                continue

    messagebox.showerror("Không thành công", "Không tìm thấy khuôn mặt trong hệ thống.")