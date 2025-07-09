import tkinter as tk
from Admin.Login_admin import render_admin_login
from Admin.Styles_admin import APP_SIZE

def start_admin_app():
    root = tk.Tk()
    root.title("Hệ thống điểm danh - Admin")
    root.geometry(APP_SIZE)
    root.resizable(False, False)

    # Frame nội dung chính (giao diện sẽ render vào đây)
    content_frame = tk.Frame(root)
    content_frame.pack(fill=tk.BOTH, expand=True)

    render_admin_login(content_frame)

    root.mainloop()

if __name__ == "__main__":
    start_admin_app()
