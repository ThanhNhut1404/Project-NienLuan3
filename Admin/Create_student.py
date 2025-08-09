import tkinter as tk
from tkinter import messagebox
import json
import threading
import cv2
from PIL import Image, ImageTk
import time
import re
import numpy as np
import hashlib

from Admin.Styles_admin import *
from Database.Create_db import insert_sinh_vien, create_table_sinh_vien, get_all_sinh_vien
from Admin.face_util import compare_face, extract_face_encodings_from_frame
from tkcalendar import DateEntry
from Admin.List_student import render_student_list

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def capitalize_name(name):
    # Split the name into words, capitalize each word, and join back
    return ' '.join(word.capitalize() for word in name.split())

def render_student_create(container, switch_to_view):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg=PAGE_BG_COLOR)
    tk.Label(container, text="👤 Đăng ký tài khoản sinh viên", font=TITLE_FONT, bg="white", fg="#003366").pack(anchor="w", padx=28, pady=(20, 5))
    create_table_sinh_vien()

    main_frame = tk.Frame(container, bg="white")
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # ========== Camera UI ==========
    camera_wrapper = tk.Frame(main_frame, bg=PAGE_BG_COLOR)
    camera_wrapper.pack(side="left", padx=(10, 5), pady=10)

    tk.Label(
        camera_wrapper,
        text=CAMERA_NOTE,
        font=CAMERA_NOTE_FONT,
        bg="white", fg="red", wraplength=440, justify="center"
    ).pack(pady=(0, 5))

    left_frame = tk.Frame(camera_wrapper, bg="black", width=460, height=360, bd=2, relief="ridge")
    left_frame.pack()
    left_frame.pack_propagate(False)
    video_label = tk.Label(left_frame, bg="black")
    video_label.pack(expand=True)

    counter_label = tk.Label(camera_wrapper, text="Đã chụp: 0/5 ảnh", bg="white", fg="#003366", font=COUNTER_FONT)
    counter_label.pack(pady=(5, 0))

    # ========== Form UI ==========
    form_wrapper = tk.Frame(
        main_frame,
        bg=FORM_BG_COLOR,
        bd=FORM_BORDER_WIDTH,
        relief=FORM_BORDER_STYLE,
        width=480,
        height=500
    )
    form_wrapper.pack(side="right", padx=10, pady=10)
    form_wrapper.pack_propagate(False)  # Ngăn khung tự co giãn theo nội dung

    form_frame = tk.Frame(form_wrapper, bg=FORM_BG_COLOR)
    form_frame.pack(padx=FORM_PADDING_X, pady=FORM_PADDING_Y)

    def make_label(text, row):
        tk.Label(form_frame, text=text, font=LABEL_FONT, bg=FORM_BG_COLOR, fg="white").grid(row=row, column=0, sticky="e", padx=FORM_LABEL_PADX, pady=5)

    def make_entry(row, show=None):
        e = tk.Entry(form_frame, font=ENTRY_FONT, width=25, show=show)
        e.grid(row=row, column=1, padx=FORM_ENTRY_PADX, pady=5)
        return e

    def only_digits(char):
        return char.isdigit()

    name_entry = make_entry(0); make_label("Họ và tên:", 0)
    class_entry = make_entry(1); make_label("Lớp:", 1)

    # MSSV
    make_label("MSSV:", 2)
    vcmd = form_frame.register(only_digits)
    mssv_entry = tk.Entry(form_frame, font=ENTRY_FONT, width=25, validate="key", validatecommand=(vcmd, "%S"))
    mssv_entry.grid(row=2, column=1, padx=FORM_ENTRY_PADX, pady=5)

    # Giới tính
    make_label("Giới tính:", 3)
    gender_var = tk.IntVar(value=1)
    gender_frame = tk.Frame(form_frame, bg=FORM_BG_COLOR)
    gender_frame.grid(row=3, column=1, padx=FORM_ENTRY_PADX, pady=5, sticky="w")

    for text, val in [("Nam", 1), ("Nữ", 0)]:
        tk.Radiobutton(
            gender_frame, text=text, variable=gender_var, value=val,
            bg=FORM_BG_COLOR, fg="white", font=ENTRY_FONT, selectcolor="black",
            activebackground=FORM_BG_COLOR, activeforeground="white"
        ).pack(side="left", padx=(0, 10))

    # Ngày sinh
    make_label("Ngày sinh:", 4)
    birth_entry = DateEntry(
        form_frame,
        date_pattern='dd-mm-yyyy',
        font=ENTRY_FONT,
        width=18,
        background='darkblue',
        foreground='white',
        borderwidth=2
    )
    birth_entry.grid(row=4, column=1, padx=FORM_ENTRY_PADX, pady=5, sticky="w")

    address_entry = make_entry(5); make_label("Địa chỉ:", 5)
    email_entry = make_entry(6); make_label("Email:", 6)
    phone_entry = make_entry(7); make_label("Số điện thoại:", 7)

    # Mật khẩu
    show_password_var = tk.BooleanVar(value=False)
    make_label("Mật khẩu:", 8)
    password_entry = tk.Entry(form_frame, font=ENTRY_FONT, width=25, show="*")
    password_entry.grid(row=8, column=1, padx=FORM_ENTRY_PADX, pady=5)

    def toggle_password():
        password_entry.config(show="" if show_password_var.get() else "*")

    tk.Checkbutton(
        form_frame,
        text="Hiện mật khẩu",
        variable=show_password_var,
        command=toggle_password,
        **CHECKBOX_STYLE
    ).grid(row=9, column=1, sticky="w", padx=FORM_ENTRY_PADX, pady=(0, 10))

    # === Logic camera, đăng ký, xử lý dữ liệu ===
    cap = None
    running = False
    capture_count = 0

    def clear_form():
        for entry in [name_entry, class_entry, mssv_entry, birth_entry, address_entry, email_entry, phone_entry,
                      password_entry]:
            entry.delete(0, tk.END)
        gender_var.set(0)  # Reset về "Nam"

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

    def show_popup(msg):
        popup = tk.Toplevel()
        popup.title("Thông báo")
        popup.geometry("300x120")
        popup.resizable(False, False)
        tk.Label(popup, text=msg, wraplength=280, justify="center", fg="red").pack(pady=15)
        tk.Button(popup, text="OK", command=popup.destroy, **POPUP_OK_BUTTON_STYLE).pack(pady=5)
        popup.grab_set()

    def register_sinh_vien():
        nonlocal capture_count
        # Họ và tên
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập họ và tên.")
            return

        # Không cho chứa số hoặc ký tự lạ
        if not re.match(r"^[A-Za-zÀ-ỹ\s]+$", name):
            messagebox.showwarning("Lỗi họ tên", "Họ tên chỉ được chứa chữ cái và khoảng trắng.")
            return

        # Tên quá ngắn
        if len(name.split()) < 2:
            messagebox.showwarning("Lỗi họ tên", "Vui lòng nhập đầy đủ họ và tên.")
            return

        # Viết hoa chữ cái đầu mỗi từ
        name = capitalize_name(name)

        mssv = mssv_entry.get().strip()
        email = email_entry.get().strip()

        # Kiểm tra định dạng email
        if not re.match(r'^[\w\.-]+@gmail\.com$', email):
            messagebox.showwarning("Lỗi định dạng Email", "Email phải có định dạng hợp lệ và kết thúc bằng @gmail.com")
            return

        # Kiểm tra MSSV và Email trùng
        for sv in get_all_sinh_vien():
            if sv["mssv"] == mssv:
                messagebox.showerror("Trùng MSSV", f"MSSV '{mssv}' đã tồn tại. Vui lòng dùng MSSV khác.")
                return
            if sv["email"] == email:
                messagebox.showerror("Trùng Email", f"Email '{email}' đã được dùng. Vui lòng chọn email khác.")
                return

        birthdate = birth_entry.get().strip()
        # Giới tính
        gender = gender_var.get()  # Lấy giá trị 0 hoặc 1
        # Số điện thoại
        phone = phone_entry.get().strip()
        if not re.match(r'^0\d{9}$', phone):
            messagebox.showwarning("Lỗi Số điện thoại", "Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0.")
            return
        # Địa chỉ
        address = address_entry.get().strip()
        if len(address) < 5:
            messagebox.showwarning("Lỗi địa chỉ", "Địa chỉ quá ngắn, vui lòng nhập đầy đủ.")
            return
        # Lớp
        class_sv = class_entry.get().strip()
        if not class_sv:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập lớp.")
            return
        # Password
        raw_password = password_entry.get().strip()
        if len(raw_password) < 6:
            messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu phải có ít nhất 6 ký tự.")
            return

        if not re.search(r'[A-Z]', raw_password):
            messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu phải chứa ít nhất 1 chữ cái in hoa.")
            return

        if not re.search(r'[a-z]', raw_password):
            messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu phải chứa ít nhất 1 chữ cái thường.")
            return

        if not re.search(r'\d', raw_password):
            messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu phải chứa ít nhất 1 số.")
            return

        if " " in raw_password:
            messagebox.showwarning("Lỗi mật khẩu", "Mật khẩu không được chứa khoảng trắng.")
            return
        password = hash_password(raw_password)

        if not all([name, mssv, email, birthdate, phone, address, class_sv, password]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tất cả các ô.")
            return

        encodings = []
        capture_count = 0
        last_capture = time.time()

        def capture_loop():
            nonlocal capture_count, last_capture
            existing = get_all_sinh_vien()  # Gọi trước khi vào while
            print(f"[DEBUG] Có {len(existing)} sinh viên trong DB để so sánh.")

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

                    # Duyệt qua danh sách sinh viên
                    for sv in existing:
                        print(f"[DEBUG] So sánh với {sv['name']} - số encoding: {len(sv['encodings'])}")
                        for known in sv.get("encodings", []):
                            try:
                                known_array = np.array(known)
                                if known_array.shape != (128,):
                                    print(f"[Bỏ qua] Encoding sai kích thước: {known_array.shape}")
                                    continue
                                if compare_face(enc, [known_array]):
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

            # Sau khi chụp đủ
            if len(encodings) < 5 or any(len(e) != 128 for e in encodings):
                stop_camera()
                show_popup("Dữ liệu khuôn mặt không hợp lệ. Vui lòng thử lại.")
                return

            try:
                insert_sinh_vien(
                    name, mssv, email, address, birthdate, gender, class_sv, password,
                    json.dumps(encodings), phone, img=""
                )
                stop_camera()
                messagebox.showinfo("Thành công", f"Tài khoản '{name}' đã được tạo thành công!")
                clear_form()
                reset_camera()
            except Exception as e:
                stop_camera()
                messagebox.showerror("Lỗi", f"Không thể lưu: {e}")

        threading.Thread(target=capture_loop).start()

    # Nút "Tạo tài khoản"
    tk.Button(
        form_frame,
        text="Tạo tài khoản",
        command=register_sinh_vien,
        **CREATE_BUTTON_STYLE
    ).grid(row=10, column=0, columnspan=2, pady=20)

    # Nút quay lại
    back_button = tk.Button(
        camera_wrapper,
        text="← Quay lại",
        command=lambda: switch_to_view("dashboard"),
        **BACK_BUTTON_STYLE
    )
    back_button.pack(anchor="w", padx=5, pady=(15, 0))

    # Khởi động camera sau khi layout xong
    container.after(500, reset_camera)
    return stop_camera  # Trả về hàm stop_camera để gọi từ bên ngoài nếu cần