import tkinter as tk
from PIL import Image, ImageTk
import os
from datetime import datetime  # 👈 Thêm để định dạng ngày

def render_view_infor(container, user):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg="white")

    # ===== FRAME CHÍNH =====
    main_frame = tk.Frame(container, bg="white")
    main_frame.pack(padx=(50, 0), pady=20, fill="both", expand=True)

    # ===== BÊN TRÁI: AVATAR =====
    left_frame = tk.Frame(main_frame, bg="white")
    left_frame.grid(row=0, column=0, sticky="n")

    # Lấy ảnh từ user["img"] nếu có, ngược lại dùng avatar mặc định
    image_path = user.get("img", "") or "avatar.png"
    if os.path.exists(image_path):
        img = Image.open(image_path)
    else:
        img = Image.new("RGB", (150, 200), color="#cccccc")  # fallback

    img = img.resize((170, 210))
    photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(left_frame, image=photo, bg="white")
    img_label.image = photo
    img_label.pack(padx=(35, 0))

    # ===== BÊN PHẢI: THÔNG TIN =====
    right_frame = tk.Frame(main_frame, bg="white")
    right_frame.grid(row=0, column=1, padx=40, sticky="nw")

    title = tk.Label(
        right_frame, text="Thông tin sinh viên",
        font=("Arial", 16, "bold"), fg="#00897B", bg="white"
    )
    title.grid(row=0, column=0, columnspan=4, pady=(0, 15), sticky="w")

    def add_pair(label1, value1, label2, value2, row):
        left_pair = tk.Frame(right_frame, bg="white")
        left_pair.grid(row=row, column=0, columnspan=2, sticky="w", pady=2, padx=(0, 40))

        tk.Label(left_pair, text=label1, font=("Arial", 11), bg="white").pack(side="left")
        tk.Label(left_pair, text=value1, font=("Arial", 11, "bold"), bg="white", fg="#00897B").pack(side="left")

        right_pair = tk.Frame(right_frame, bg="white")
        right_pair.grid(row=row, column=2, columnspan=2, sticky="w", pady=2)

        tk.Label(right_pair, text=label2, font=("Arial", 11), bg="white").pack(side="left")
        tk.Label(right_pair, text=value2, font=("Arial", 11, "bold"), bg="white", fg="#00897B").pack(side="left")

    # ===== Định dạng ngày sinh: yyyy-mm-dd -> dd-mm-yyyy =====
    raw_date = user.get("date", "")
    try:
        formatted_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%d-%m-%Y")
    except:
        formatted_date = raw_date  # fallback nếu lỗi

    # ===== CÁC DÒNG HIỂN THỊ =====
    add_pair("MSSV:", user.get("mssv", ""), "Địa chỉ:", user.get("address", ""), 1)
    add_pair("Họ tên:", user.get("name", ""), "Lớp học:", user.get("class", ""), 2)
    add_pair("Giới tính:", "Nam" if user.get("sex") == 1 else "Nữ", "Email:", user.get("email", ""), 3)
    add_pair("Ngày sinh:", formatted_date, "Số điện thoại:", user.get("phone", ""), 4)
