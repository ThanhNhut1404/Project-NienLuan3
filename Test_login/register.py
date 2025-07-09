# register.py
import tkinter as tk
from tkinter import messagebox
from database import init_db, insert_user, user_exists, get_all_users
from face_utils import capture_multiple_encodings, compare_face
def show_custom_popup(message):
    popup = tk.Toplevel()
    popup.title("Thông báo")
    popup.geometry("300x120")
    popup.resizable(False, False)

    tk.Label(popup, text=message, wraplength=280, justify="center", fg="red").pack(pady=15)
    tk.Button(popup, text="OK", command=popup.destroy, bg="#f44336", fg="white", width=10).pack(pady=5)

    popup.grab_set()  # Khóa popup cho đến khi tắt
def register_user():
    name = name_entry.get().strip()
    user_id = id_entry.get().strip()
    email = email_entry.get().strip()
    birthdate = birth_entry.get().strip()
    gender = gender_entry.get().strip()
    phone = phone_entry.get().strip()

    if not all([name, user_id, email, birthdate, gender, phone]):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tất cả thông tin.")
        return

    if user_exists(user_id, name):
        messagebox.showerror("Đã tồn tại", f"Người dùng với ID '{user_id}' và tên '{name}' đã tồn tại.\nVui lòng nhập ID hoặc tên khác.")
        return

    known_users = get_all_users()
    encodings = capture_multiple_encodings()

    if not encodings:
        messagebox.showerror("Thất bại", "Không lấy được dữ liệu khuôn mặt.")
        return

    # ✅ Kiểm tra nếu gương mặt trùng với người đã có
    for encoding_json in encodings:
        matched = compare_face(encoding_json, known_users)
        if matched:
            show_custom_popup(f"Gương mặt đã được đăng ký bởi {matched[1]} (ID: {matched[0]}).\nKhông thể đăng ký lại.")

            return

    # ✅ Nếu không trùng, lưu dữ liệu
    for encoding_json in encodings:
        insert_user(user_id, name, email, birthdate, gender, phone, encoding_json)

    messagebox.showinfo("Thành công", f"Đã lưu {len(encodings)} ảnh cho {name}")

# Khởi tạo CSDL
init_db()

# Giao diện Tkinter
root = tk.Tk()
root.title("Đăng ký người dùng bằng khuôn mặt")
root.geometry("400x350")
root.resizable(False, False)

tk.Label(root, text="Họ tên:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Mã người dùng:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
id_entry = tk.Entry(root, width=30)
id_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Ngày sinh (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
birth_entry = tk.Entry(root, width=30)
birth_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Giới tính (Nam/Nữ):").grid(row=4, column=0, padx=10, pady=5, sticky='e')
gender_entry = tk.Entry(root, width=30)
gender_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Số điện thoại:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
phone_entry = tk.Entry(root, width=30)
phone_entry.grid(row=5, column=1, padx=10, pady=5)

# Nút đăng ký
btn = tk.Button(root, text="Đăng ký khuôn mặt", command=register_user, font=("Arial", 12), bg="#4CAF50", fg="white")
btn.grid(row=6, column=0, columnspan=2, pady=15)

root.mainloop()
