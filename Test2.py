import tkinter as tk


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giao diện đẹp với Tkinter")
root.geometry("400x300")
root.configure(bg="#f0f4f8")

# Font và màu sắc chính
MAIN_COLOR = "#3498db"
HOVER_COLOR = "#2980b9"
TEXT_COLOR = "#ffffff"
FONT = ("Segoe UI", 12)

# Tiêu đề
title_label = tk.Label(root, text="Chào mừng bạn đến với ứng dụng!", font=("Segoe UI", 16, "bold"), bg="#f0f4f8", fg="#2c3e50")
title_label.pack(pady=20)

# Hàm xử lý khi nhấn nút
def on_click(name):
    result_label.config(text=f"Bạn đã chọn: {name}")

# Tạo nút có hiệu ứng hover
def create_hover_button(parent, text, command):
    btn = tk.Label(parent, text=text, bg=MAIN_COLOR, fg=TEXT_COLOR, font=FONT, padx=20, pady=10, cursor="hand2")
    btn.pack(pady=5)

    def on_enter(e):
        btn.config(bg=HOVER_COLOR)

    def on_leave(e):
        btn.config(bg=MAIN_COLOR)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", lambda e: command())

    return btn

# Tạo các nút
create_hover_button(root, "Trang Chủ", lambda: on_click("Trang Chủ"))
create_hover_button(root, "Giới Thiệu", lambda: on_click("Giới Thiệu"))
create_hover_button(root, "Thoát", root.quit)

# Nhãn kết quả
result_label = tk.Label(root, text="", font=("Segoe UI", 12), bg="#f0f4f8", fg="#2c3e50")
result_label.pack(pady=10)

# Chạy giao diện
root.mainloop()
