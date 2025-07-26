import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import cv2
import numpy as np
import face_recognition
import sqlite3
import datetime
from Database.Create_db import DB_NAME
from Student.Styles_student import BACK_BUTTON_STYLE
from Student.View_activity import render_view_activity

def render_activity_roll_call(container, user, go_back=None):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg="white")

    tk.Label(container, text="🔍 Điểm danh hoạt động", font=("Arial", 16, "bold"), bg="white", fg="#00897B") \
        .pack(pady=10, anchor="w",  padx=70)

    tk.Label(container, text="Bấm nút bên dưới để hệ thống nhận diện khuôn mặt và quét mã QR.",
             font=("Arial", 13), bg="white", fg="red").pack(pady=10)
    # ========== CAMERA FRAME ==========
    camera_frame = tk.Frame(
        container,
        bg="black",
        width=600,
        height=375,
        bd=3,
        relief="ridge"
    )
    camera_frame.pack(pady=10)
    camera_frame.pack_propagate(False)

    video_label = tk.Label(camera_frame, bg="black")
    video_label.pack(expand=True)

    # ========== KHUNG DƯỚI CHỨA 2 NÚT: QUAY LẠI & ĐIỂM DANH ========== ✅
    bottom_frame = tk.Frame(container, bg="white")
    bottom_frame.pack(fill="x", side="bottom", padx=20, pady=10)

    # Nút Quay lại: nằm sát bên trái
    back_btn = tk.Button(
        bottom_frame,
        text="← Quay lại",
        command=lambda: render_view_activity(container, user),  # 🟢 Gọi lại trang hoạt động
        **BACK_BUTTON_STYLE
    )
    back_btn.pack(side="left", anchor="w")


    roll_call_btn = tk.Button(
        bottom_frame,
        text="Bắt đầu điểm danh",
        font=("Arial", 12, "bold"),
        activebackground="#FF5722",
        command=lambda: start_roll_call(user, video_label),
        bg="#FFA726", fg="white", padx=10, pady=5
    )
    roll_call_btn.pack()

    bottom_frame.update_idletasks()
    roll_call_btn.place(relx=0.5, rely=0.5, anchor="center")


def start_roll_call(user, video_label):
    mssv = user["mssv"]
    known_encodings = [np.array(enc) for enc in user.get("encodings", [])]

    if not known_encodings:
        messagebox.showerror("Lỗi", "Sinh viên chưa có dữ liệu khuôn mặt.")
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = cv2.QRCodeDetector()

    face_verified = False
    qr_data = None
    timeout = 20
    start_time = datetime.datetime.now()

    def update():
        nonlocal face_verified, qr_data

        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # ===== Nhận diện khuôn mặt =====
                face_encodings = face_recognition.face_encodings(rgb)
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.45)
                    if matches.count(True) > 0:
                        face_verified = True
                        break

                if face_verified:
                    data, bbox, _ = detector.detectAndDecode(frame)
                    if bbox is not None and data and data.startswith("HOATDONG:"):
                        qr_data = data.replace("HOATDONG:", "")
                        finish()
                        return

                # ===== Hiển thị lên video_label =====
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                video_label.imgtk = imgtk
                video_label.configure(image=imgtk)

        if (datetime.datetime.now() - start_time).total_seconds() > timeout:
            finish()
            return

        video_label.after(10, update)

    def finish():
        cap.release()
        video_label.config(image="")

        if not face_verified:
            messagebox.showwarning("Thất bại", "Không xác minh được khuôn mặt.")
            return

        if not qr_data:
            messagebox.showwarning("Thất bại", "Không quét được mã QR hợp lệ.")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT TEN_HD, START_TIME, TIME_OUT, NGAY_TO_CHUC, DIEM_CONG, id_hk
                FROM HOAT_DONG
                WHERE ID_HD = ?
            ''', (qr_data,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Lỗi", "Không tìm thấy hoạt động tương ứng.")
                return

            ten_hd, start_time_str, end_time_str, ngay_str, diem_cong, id_hk = row
            start_dt = datetime.datetime.strptime(f"{ngay_str} {start_time_str}", "%d/%m/%Y %H:%M:%S")
            end_dt = datetime.datetime.strptime(f"{ngay_str} {end_time_str}", "%d/%m/%Y %H:%M:%S")
            now = datetime.datetime.now()

            if not (start_dt <= now <= end_dt):
                messagebox.showwarning("Quá thời gian", f"Hoạt động '{ten_hd}' chưa bắt đầu hoặc đã kết thúc.")
                return

            cursor.execute('''
                SELECT 1 FROM DIEM_DANH_HOAT_DONG
                WHERE id_hoat_dong = ? AND MSSV = ?
            ''', (qr_data, mssv))
            if cursor.fetchone():
                messagebox.showinfo("Thông báo", f"Bạn đã điểm danh hoạt động '{ten_hd}' trước đó.")
                return

            cursor.execute('''
                INSERT INTO DIEM_DANH_HOAT_DONG (id_hoat_dong, MSSV, thoi_gian, diem_cong, id_hk)
                VALUES (?, ?, ?, ?, ?)
            ''', (qr_data, mssv, now.strftime("%Y-%m-%d %H:%M:%S"), diem_cong, id_hk))

            cursor.execute('''
                UPDATE SINH_VIEN SET TONG_DIEM_HD = IFNULL(TONG_DIEM_HD, 0) + ?
                WHERE MSSV = ?
            ''', (diem_cong, mssv))

            conn.commit()
            messagebox.showinfo("Thành công", f"Đã điểm danh thành công hoạt động '{ten_hd}'")

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", str(e))
        finally:
            conn.close()

    update()
