import tkinter as tk
from tkinter import messagebox
import json
import cv2
import face_recognition
import numpy as np
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

    # ========== FRAME TRÁI: CAMERA + NÚT ĐĂNG NHẬP KHUÔN MẶT ========== #
    left_frame = tk.Frame(container, bg="white", bd=2, relief="ridge")
    left_frame.place(relx=0.02, rely=0.05, relwidth=0.46, relheight=0.9)

    tk.Label(
        left_frame,
        text="QUÉT KHUÔN MẶT",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#003366"
    ).pack(pady=(15, 10))

    cam_label = tk.Label(left_frame, bg="white", relief="sunken", bd=1)
    cam_label.pack(padx=10, pady=10, fill="both", expand=True)

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

    # --- NÚT ĐĂNG NHẬP BẰNG KHUÔN MẶT --- #
    tk.Button(
        left_frame,
        text="🧑‍💻 Đăng nhập bằng khuôn mặt",
        command=lambda: face_login(current_frame, cap, container),
        **BUTTON_STYLE
    ).pack(pady=(20, 10))

    # ========== FRAME PHẢI: ĐĂNG NHẬP TÀI KHOẢN ========== #
    right_frame = tk.Frame(container, bg="white", bd=2, relief="ridge")
    right_frame.place(relx=0.51, rely=0.05, relwidth=0.47, relheight=0.9)

    tk.Label(
        right_frame,
        text="ĐĂNG NHẬP BẰNG TÀI KHOẢN",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#003366"
    ).pack(pady=(30, 20))

    # --- Biểu mẫu đăng nhập --- #
    form_frame = tk.Frame(right_frame, bg="white")
    form_frame.pack(pady=(10, 0))

    tk.Label(form_frame, text="MSSV:", bg="white", font=LABEL_FONT).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    mssv_entry = tk.Entry(form_frame, font=ENTRY_FONT, width=30)
    mssv_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Mật khẩu:", bg="white", font=LABEL_FONT).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    password_entry = tk.Entry(form_frame, show="*", font=ENTRY_FONT, width=30)
    password_entry.grid(row=1, column=1, pady=5)

    def login_by_account():
        mssv = mssv_entry.get().strip()
        password = password_entry.get().strip()

        if not mssv or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ MSSV và mật khẩu.")
            return

        all_users = get_all_sinh_vien()
        for user in all_users:
            if user["mssv"] == mssv and user.get("password") == password:
                cap.release()
                render_student_main(container, user)
                return

        messagebox.showerror("Lỗi", "Sai MSSV hoặc mật khẩu.")

    # --- Nút đăng nhập tài khoản --- #
    tk.Button(
        right_frame,
        text="🔓 Đăng nhập",
        command=login_by_account,
        **BUTTON_STYLE
    ).pack(pady=(30, 10))

    # ========== ĐÓNG ỨNG DỤNG ========== #
    container.winfo_toplevel().protocol(
        "WM_DELETE_WINDOW",
        lambda: (cap.release(), container.winfo_toplevel().destroy())
    )



# ===================== ĐĂNG NHẬP BẰNG KHUÔN MẶT ===================== #
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
                match = face_recognition.compare_faces([known_np], unknown_encoding, tolerance=0.5)[0]
                if match:
                    cap.release()
                    render_student_main(container, user)
                    return
            except Exception as e:
                print("[Lỗi] So sánh encoding:", e)
                continue

    messagebox.showerror("Không thành công", "Không tìm thấy khuôn mặt trong hệ thống.")
