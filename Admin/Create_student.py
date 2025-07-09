import tkinter as tk
from Admin.Styles_admin import TITLE_FONT, LABEL_FONT, ENTRY_FONT, BUTTON_STYLE
from tkinter import messagebox
from Database.Create_db import insert_sinh_vien,sinh_vien_exists, get_all_sinh_vien,create_table_sinh_vien
from face_util import capture_multiple_encodings, compare_face
def show_popup(message):
    popup = tk.Toplevel()
    popup.title("Thông báo")
    popup.geometry("300x120")
    popup.resizable(False, False)

    tk.Label(popup, text=message, wraplength=280, justify="center", fg="red").pack(pady=15)
    tk.Button(popup, text="OK", command=popup.destroy, bg="#f44336", fg="white", width=10).pack(pady=5)
    popup.grab_set()  # Khóa popup cho đến khi tắt
def register_sinh_vien():
    name = name_entry.get().strip()
    mssv = mssv_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()
    birthdate = birth_entry.get().strip()
    gender = gender_entry.get().strip()   # Nhập 0 (Nam) hoặc 1 (Nữ)
    class_sv = class_entry.get().strip()
    password = password_entry.get().strip()

    # ⚠️ Kiểm tra thông tin cần thiết
    if not all([name,mssv,email, address, birthdate, gender, class_sv, password]):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tất cả các trường.")
        return
    if sinh_vien_exists(name):
        messagebox.showerror("Đã tồn tại", f"Người dùng với tên '{name}' đã tồn tại.\nVui lòng nhập tên khác.")
        return
    # ⚠️ Lấy danh sách sinh viên đã có
    known_users = get_all_sinh_vien()

    # 🧠 Chụp nhiều lần để lấy encoding
    encodings = capture_multiple_encodings()
    if not encodings:
        messagebox.showerror("Thất bại", "Không lấy được dữ liệu khuôn mặt.")
        return

    # ✅ Kiểm tra trùng khuôn mặt
    for encoding_json in encodings:
        matched = compare_face(encoding_json, known_users)
        if matched:
            show_popup(f"Gương mặt đã được đăng ký bởi {matched['name']} .\nKhông thể đăng ký lại.")
            return

    # ✅ Nếu không trùng, lưu nhiều dòng (mỗi face_encoding 1 dòng)
    try:
        for encoding_json in encodings:
            insert_sinh_vien(name,mssv, email, address, birthdate, gender, class_sv, password, encoding_json)
        messagebox.showinfo("Thành công", f"Đã lưu {len(encodings)} ảnh cho {name}")
        print(f"✅ Sinh viên '{name}' đã được đăng ký thành công cùng {len(encodings)} ảnh.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")


# Khởi tạo CSDL
create_table_sinh_vien()
# Giao diện Tkinter
# Giao diện Tkinter
root = tk.Tk()
root.title("Đăng ký người dùng bằng khuôn mặt")
root.geometry("400x500")
root.resizable(False, False)

tk.Label(root, text="Họ tên:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="MSSV:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
mssv_entry = tk.Entry(root, width=30)
mssv_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Ngày sinh (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
birth_entry = tk.Entry(root, width=30)
birth_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Giới tính (0 = Nam / 1 = Nữ):").grid(row=4, column=0, padx=10, pady=5, sticky='e')
gender_entry = tk.Entry(root, width=30)
gender_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Số điện thoại:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
phone_entry = tk.Entry(root, width=30)
phone_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Địa chỉ:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
address_entry = tk.Entry(root, width=30)
address_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Lớp:").grid(row=7, column=0, padx=10, pady=5, sticky='e')
class_entry = tk.Entry(root, width=30)
class_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Mật khẩu:").grid(row=8, column=0, padx=10, pady=5, sticky='e')
password_entry = tk.Entry(root, width=30, show="*")
password_entry.grid(row=8, column=1, padx=10, pady=5)

btn = tk.Button(root, text="Đăng ký khuôn mặt", command=register_sinh_vien, font=("Arial", 12), bg="#4CAF50", fg="white")
btn.grid(row=9, column=0, columnspan=2, pady=15)

root.mainloop()
