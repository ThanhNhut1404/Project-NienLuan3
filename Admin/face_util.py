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

    left_frame = tk.Frame(container, bg="white", bd=2, relief="groove")
    left_frame.place(relx=0.02, rely=0.05, relwidth=0.45, relheight=0.9)
    tk.Label(left_frame, text="CAMERA NHẬN DIỆN KHUÔN MẶT", font=("Arial", 14, "bold"), bg="white").pack(pady=(15, 5))
    cam_label = tk.Label(left_frame, bg="white")
    cam_label.pack()

    current_frame = {'image': None}

    def update_camera():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (360, 270))
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            current_frame['image'] = rgb_frame
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            cam_label.imgtk = imgtk
            cam_label.configure(image=imgtk)
        cam_label.after(10, update_camera)

    update_camera()

    right_frame = tk.Frame(container, bg="white", bd=2, relief="groove")
    right_frame.place(relx=0.52, rely=0.3, relwidth=0.45, relheight=0.4)
    tk.Button(
        right_frame,
        text="Đăng nhập bằng khuôn mặt",
        command=lambda: face_login(current_frame, cap, container),
        **BUTTON_STYLE
    ).pack(expand=True)

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
        raw = user.get("encoding_json") or user.get("face_encoding") or user.get("encoding")
        if not raw:
            continue
        try:
            enc_list = json.loads(raw)
            if isinstance(enc_list[0], str):
                enc_list = [json.loads(item) for item in enc_list]
        except Exception as e:
            print("[Lỗi] Load encoding JSON:", e)
            continue

        for known_encoding in enc_list:
            try:
                known_np = np.array(known_encoding, dtype=np.float64)
                match = face_recognition.compare_faces([known_np], unknown_encoding, tolerance=0.5)[0]
                if match:
                    cap.release()
                    messagebox.showinfo("Thành công", f"Xin chào {user.get('name', 'sinh viên')}!")
                    render_student_main(container)
                    return
            except Exception as e:
                print("[Lỗi] So sánh encoding:", e)
                continue

    messagebox.showerror("Không thành công", "Không tìm thấy khuôn mặt trong hệ thống.")
