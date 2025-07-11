import tkinter as tk
from tkinter import messagebox
import json
import threading
import cv2
from PIL import Image, ImageTk
import time
import numpy as np

from Student.Styles_student import *
from Database.Create_db import insert_sinh_vien, create_table_sinh_vien, get_all_sinh_vien
from Admin.face_util import compare_face, extract_face_encodings_from_frame


def render_student_create(container):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg=PAGE_BG_COLOR)
    tk.Label(container, text="Đăng ký tài khoản sinh viên", font=TITLE_FONT, bg="white", fg="#003366").pack(pady=(20, 10))
    create_table_sinh_vien()

    main_frame = tk.Frame(container, bg="white")
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # ===== Camera UI =====
    camera_wrapper = tk.Frame(main_frame, bg=PAGE_BG_COLOR)
    camera_wrapper.pack(side="left", padx=(10, 5), pady=10)
    tk.Label(
        camera_wrapper,
        text="Camera sẽ bắt đầu chụp sau khi nhấn 'Tạo tài khoản'.\nHệ thống sẽ chụp 5 ảnh khuôn mặt. Hãy nhìn thẳng vào camera.",
        font=("Arial", 11, "italic"),
        bg="white", fg="red", wraplength=440, justify="center"
    ).pack(pady=(0, 5))

    left_frame = tk.Frame(camera_wrapper, bg="black", width=460, height=360, bd=2, relief="ridge")
    left_frame.pack(); left_frame.pack_propagate(False)
    video_label = tk.Label(left_frame, bg="black"); video_label.pack(expand=True)

    counter_label = tk.Label(camera_wrapper, text="Đã chụp: 0/5 ảnh", bg="white", fg="#003366", font=("Arial", 14, "bold"))
    counter_label.pack(pady=(5, 0))

    # ===== Form UI =====
    form_wrapper = tk.Frame(main_frame, bg=FORM_BG_COLOR, bd=FORM_BORDER_WIDTH, relief=FORM_BORDER_STYLE)
    form_wrapper.pack(side="right", padx=10, pady=10)
    form_frame = tk.Frame(form_wrapper, bg=FORM_BG_COLOR)
    form_frame.pack(padx=FORM_PADDING_X, pady=FORM_PADDING_Y)

    def make_label(text, row):
        tk.Label(form_frame, text=text, font=LABEL_FONT, bg=FORM_BG_COLOR, fg="white").grid(row=row, column=0, sticky="e", padx=5, pady=5)

    def make_entry(row, show=None):
        e = tk.Entry(form_frame, font=ENTRY_FONT, width=25, show=show)
        e.grid(row=row, column=1, padx=5, pady=5)
        return e

    name_entry = make_entry(0); make_label("Họ và tên:", 0)
    class_entry = make_entry(1); make_label("Lớp:", 1)
    mssv_entry = make_entry(2); make_label("MSSV:", 2)
    gender_entry = make_entry(3); make_label("Giới tính:", 3)
    birth_entry = make_entry(4); make_label("Ngày sinh:", 4)
    address_entry = make_entry(5); make_label("Địa chỉ:", 5)
    email_entry = make_entry(6); make_label("Email:", 6)
    phone_entry = make_entry(7); make_label("Số điện thoại:", 7)
    password_entry = make_entry(8, show="*"); make_label("Mật khẩu:", 8)

    cap = None
    running = False
    capture_count = 0

    def clear_form():
        for entry in [name_entry, class_entry, mssv_entry, gender_entry, birth_entry, address_entry, email_entry, phone_entry, password_entry]:
            entry.delete(0, tk.END)

    def stop_camera():
        nonlocal cap, running
        running = False
        if cap and cap.isOpened():
            cap.release()
            cap = None
        video_label.config(image='')

    def reset_camera():
        nonlocal cap, running, capture_count
        capture_count = 0
        counter_label.config(text="Đã chụp: 0/5 ảnh")
        stop_camera()
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        running = True
        update_camera()

    def update_camera():
        if running and cap and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (460, 360))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                video_label.imgtk = imgtk
                video_label.configure(image=imgtk)
        if running:
            video_label.after(10, update_camera)

    reset_camera()

    def show_popup(msg):
        popup = tk.Toplevel()
        popup.title("Thông báo")
        popup.geometry("300x120")
        popup.resizable(False, False)
        tk.Label(popup, text=msg, wraplength=280, justify="center", fg="red").pack(pady=15)
        tk.Button(popup, text="OK", command=popup.destroy, bg="#f44336", fg="white", width=10).pack(pady=5)
        popup.grab_set()

    def register_sinh_vien():
        nonlocal capture_count
        name = name_entry.get().strip()
        mssv = mssv_entry.get().strip()
        email = email_entry.get().strip()
        birthdate = birth_entry.get().strip()
        gender = gender_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip()
        class_sv = class_entry.get().strip()
        password = password_entry.get().strip()

        if not all([name, mssv, email, birthdate, gender, phone, address, class_sv, password]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tất cả các trường.")
            return

        encodings = []
        capture_count = 0
        last_capture = time.time()

        def capture_loop():
            nonlocal capture_count, last_capture
            while capture_count < 5 and cap and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    continue
                if time.time() - last_capture >= 1.5:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    enc = extract_face_encodings_from_frame(frame_rgb)

                    if not enc or not isinstance(enc, list) or len(enc) != 128:
                        print("[Lỗi] Encoding mới không hợp lệ, bỏ qua ảnh này.")
                        continue

                    existing = get_all_sinh_vien()
                    print(f"[DEBUG] Có {len(existing)} sinh viên trong DB để so sánh.")
                    for sv in existing:
                        print(f"[DEBUG] So sánh với {sv['name']} - số encoding: {len(sv['encodings'])}")
                        for known in sv.get("encodings", []):
                            try:
                                known = np.array(known)
                                if known.shape != (128,):
                                    print(f"[Bỏ qua] Encoding sai kích thước: {known.shape}")
                                    continue
                                if compare_face(enc, [known]):
                                    stop_camera()
                                    show_popup(f"Gương mặt đã tồn tại: {sv['name']}. Vui lòng dùng khuôn mặt khác.")
                                    reset_camera()
                                    return
                            except Exception as e:
                                print("[Lỗi] So sánh khuôn mặt:", e)

                    encodings.append(enc)
                    capture_count += 1
                    counter_label.config(text=f"Đã chụp: {capture_count}/5 ảnh")
                    last_capture = time.time()

            stop_camera()

            if not encodings or any(len(e) != 128 for e in encodings):
                show_popup("Dữ liệu khuôn mặt không hợp lệ. Vui lòng thử lại.")
                return

            try:
                insert_sinh_vien(
                    name, mssv, email, address, birthdate, gender, class_sv, password,
                    json.dumps(encodings)
                )
                messagebox.showinfo("Thành công", f"Tài khoản '{name}' đã được tạo thành công!")
                clear_form()
                reset_camera()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu: {e}")

        threading.Thread(target=capture_loop).start()

    tk.Button(form_frame, text="Tạo tài khoản", command=register_sinh_vien, **BUTTON_STYLE).grid(row=10, column=0, columnspan=2, pady=20)
