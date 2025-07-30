import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
import os
from Admin.Styles_admin import *

def show_qr_image(container, qr_path):
    for widget in container.winfo_children():
        widget.destroy()

    container.config(bg=PAGE_BG_COLOR)

    # ====== Tiêu đề ======
    tk.Label(container, text="🖼 Mã QR hoạt động", font=TITLE_FONT, bg="white", fg="#003366").pack(
        anchor="w", padx=28, pady=(20, 5)
    )

    try:
        img = Image.open(qr_path)
        img = img.resize((450, 450))
        photo = ImageTk.PhotoImage(img)

        # ====== Khung chứa QR và nút lưu về máy (canh giữa) ======
        qr_frame = tk.Frame(container, bg=PAGE_BG_COLOR)
        qr_frame.pack(pady=10)

        img_label = tk.Label(qr_frame, image=photo, bg=PAGE_BG_COLOR)
        img_label.image = photo  # giữ tham chiếu
        img_label.pack()

        btn_save = tk.Button(
            qr_frame,
            text="📥 Lưu về máy",
            command=lambda: save_qr(),
            **CREATE_BUTTON_STYLE
        )
        btn_save.pack(pady=(10, 0))

    except Exception as e:
        tk.Label(container, text=f"Lỗi khi hiển thị ảnh: {e}", fg="red").pack()

    def save_qr():
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=os.path.basename(qr_path)
        )
        if save_path:
            try:
                shutil.copy(qr_path, save_path)
                messagebox.showinfo("Thành công", f"Đã lưu mã QR tại:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def back_to_main():
        from Admin.Create_activity import render_Create_activity
        render_Create_activity(container)

    # ====== Nút Quay lại nằm sát góc trái dưới cùng ======
    btn_back = tk.Button(
        container,
        text="← Quay lại",
        command=back_to_main,
        **BACK_BUTTON_STYLE
    )
    btn_back.place(relx=0.0, rely=1.0, anchor="sw", x=28, y=-10)
