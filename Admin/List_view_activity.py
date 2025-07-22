import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from Admin.Edit_activity import render_edit_activity

DB_NAME = "Database/Diem_danh.db"

def render_view_activities(container, go_back):
    for widget in container.winfo_children():
        widget.destroy()

    def load_activities():
        for item in tree.get_children():
            tree.delete(item)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT ID_HD, TEN_HD, NGAY_TO_CHUC, START_TIME, TIME_OUT FROM HOAT_DONG")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", "end", values=row)

    def handle_delete():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một hoạt động để xóa.")
            return

        selected_values = tree.item(selected_item, 'values')
        if not selected_values:
            return

        try:
            id_hd = int(selected_values[0])
        except ValueError:
            messagebox.showerror("Lỗi", "Không xác định được ID hoạt động.")
            return

        # Lấy ngày tổ chức và giờ bắt đầu để kiểm tra
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT NGAY_TO_CHUC, START_TIME FROM HOAT_DONG WHERE ID_HD = ?", (id_hd,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            messagebox.showerror("Lỗi", "Không tìm thấy hoạt động.")
            return

        ngay_to_chuc_str, start_time_str = result

        try:
            # ✅ Lưu ý: sửa định dạng ngày thành "%d/%m/%Y" cho đúng với dữ liệu lưu trong DB
            full_datetime = datetime.strptime(f"{ngay_to_chuc_str} {start_time_str}", "%d/%m/%Y %H:%M:%S")
        except ValueError:
            messagebox.showerror("Lỗi định dạng thời gian", f"Không thể đọc thời gian hoạt động.\nNgày: {ngay_to_chuc_str}, Giờ: {start_time_str}")
            return

        if full_datetime <= datetime.now():
            messagebox.showinfo("Không thể xóa", "Chỉ được xóa hoạt động chưa diễn ra.")
            return

        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa hoạt động này?")
        if confirm:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM HOAT_DONG WHERE ID_HD = ?", (id_hd,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Đã xóa hoạt động.")
            load_activities()

    def handle_edit():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một hoạt động để sửa.")
            return

        selected_values = tree.item(selected_item, 'values')
        if not selected_values:
            return

        try:
            id_hd = int(selected_values[0])
        except ValueError:
            messagebox.showerror("Lỗi", "Không xác định được ID hoạt động.")
            return

        render_edit_activity(container, id_hd, lambda: render_view_activities(container, go_back))

    def handle_back():
        if go_back:
            go_back()

    # ========== TITLE ==========
    tk.Label(container, text="Danh sách hoạt động", font=("Helvetica", 16, "bold")).pack(pady=10)

    # ========== TREEVIEW ==========
    columns = ("ID", "Tên hoạt động", "Ngày tổ chức", "Giờ bắt đầu", "Giờ kết thúc")
    tree = ttk.Treeview(container, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # ========== BUTTON ==========
    btn_frame = tk.Frame(container)
    btn_frame.pack(pady=10)

    btn_edit = tk.Button(btn_frame, text="Sửa hoạt động", bg="#4caf50", fg="white", width=15, command=handle_edit)
    btn_edit.grid(row=0, column=0, padx=5)

    btn_delete = tk.Button(btn_frame, text="Xóa hoạt động", bg="#f44336", fg="white", width=15, command=handle_delete)
    btn_delete.grid(row=0, column=1, padx=5)

    btn_back = tk.Button(btn_frame, text="Quay lại", width=15, command=handle_back)
    btn_back.grid(row=0, column=2, padx=5)

    # ========== LOAD DATA ==========
    load_activities()
