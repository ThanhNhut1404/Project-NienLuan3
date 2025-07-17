import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import face_recognition
import sqlite3
import datetime
from Database.Create_db import DB_NAME


def start_roll_call(user):
    mssv = user["mssv"]
    known_encodings = [np.array(enc) for enc in user.get("encodings", [])]

    if not known_encodings:
        messagebox.showerror("Lỗi", "Sinh viên chưa có dữ liệu khuôn mặt.")
        return

    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    qr_data = None
    face_verified = False
    timeout = 20
    start_time = datetime.datetime.now()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
                break

        if (datetime.datetime.now() - start_time).total_seconds() > timeout:
            break

        cv2.imshow("Điểm danh hoạt động", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if not face_verified:
        messagebox.showwarning("Thất bại", "Không xác minh được khuôn mặt.")
        return

    if not qr_data:
        messagebox.showwarning("Thất bại", "Không quét được mã QR hợp lệ.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Lấy thông tin hoạt động kèm ID học kỳ
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

        # Kiểm tra đã điểm danh chưa
        cursor.execute('''
            SELECT 1 FROM DIEM_DANH_HOAT_DONG
            WHERE id_hoat_dong = ? AND MSSV = ?
        ''', (qr_data, mssv))
        if cursor.fetchone():
            messagebox.showinfo("Thông báo", f"Bạn đã điểm danh hoạt động '{ten_hd}' trước đó.")
            return

        # Ghi điểm danh
        cursor.execute('''
            INSERT INTO DIEM_DANH_HOAT_DONG (id_hoat_dong, MSSV, thoi_gian, diem_cong, id_hk)
            VALUES (?, ?, ?, ?, ?)
        ''', (qr_data, mssv, now.strftime("%Y-%m-%d %H:%M:%S"), diem_cong, id_hk))

        # Cộng điểm cho sinh viên
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


def open_activity_roll_call(user):
    window = tk.Toplevel()
    window.title("Điểm danh hoạt động")
    window.geometry("400x200")
    window.resizable(False, False)

    label = tk.Label(window, text="Nhấn để bắt đầu điểm danh bằng khuôn mặt và mã QR", font=("Arial", 11))
    label.pack(pady=20)

    btn = tk.Button(window, text="Bắt đầu điểm danh", font=("Arial", 12, "bold"), command=lambda: start_roll_call(user))
    btn.pack(pady=10)

    window.mainloop()
