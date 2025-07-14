import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
import os

def show_qr_image(container, qr_path):
    for widget in container.winfo_children():
        widget.destroy()

    # ====== Hiển thị QR ======
    tk.Label(container, text="🖼 MÃ QR HOẠT ĐỘNG", font=("Arial", 16, "bold"), fg="#003366").pack(pady=10)

    try:
        img = Image.open(qr_path)
        img = img.resize((300, 300))
        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(container, image=photo)
        img_label.image = photo  # giữ tham chiếu
        img_label.pack(pady=10)
    except Exception as e:
        tk.Label(container, text=f"Lỗi khi hiển thị ảnh: {e}", fg="red").pack()

    # ====== Nút lưu về ======
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

    tk.Button(container, text="📥 Lưu về máy", command=save_qr,
              font=("Arial", 11), bg="#006699", fg="white").pack(pady=15)
