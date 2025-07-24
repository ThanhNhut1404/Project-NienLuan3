import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from Admin.Styles_admin import *
from Admin.Edit_activity import render_edit_activity

DB_NAME = "Database/Diem_danh.db"

def render_view_activities(container, go_back):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg=PAGE_BG_COLOR)

    # ========== MAIN WRAPPER ==========
    wrapper = tk.Frame(container, bg=PAGE_BG_COLOR)
    wrapper.pack(fill=tk.BOTH, expand=True)

    # ========== TITLE ==========
    title_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    title_frame.pack(anchor="w", padx=28, pady=(20, 5))
    tk.Label(title_frame, text="Danh sách hoạt động", font=TITLE_FONT, bg="white", fg="#003366").pack(anchor="w")

    # ========== TREEVIEW ==========
    tree_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 5))

    style = ttk.Style()
    style.theme_use("default")

    # Ẩn border viền xung quanh
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    style.configure("Treeview",
                    font=TREEVIEW_STYLE["font"],
                    rowheight=TREEVIEW_STYLE["rowheight"],
                    background="white",
                    foreground="black",
                    fieldbackground="white")

    style.configure("Treeview.Heading",
                    font=TREEVIEW_STYLE["header_font"],
                    background=TREEVIEW_STYLE["header_bg"],
                    foreground=TREEVIEW_STYLE["header_fg"])

    # Ngăn hover header sáng
    style.map("Treeview.Heading", background=[("active", TREEVIEW_STYLE["header_bg"])])

    columns = ("ID", "Tên hoạt động", "Ngày tổ chức", "Giờ bắt đầu", "Giờ kết thúc")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("ID", text="ID")
    tree.column("ID", anchor="center", width=25)

    tree.heading("Tên hoạt động", text="Tên hoạt động")
    tree.column("Tên hoạt động", anchor="w", width=270)

    tree.heading("Ngày tổ chức", text="Ngày tổ chức")
    tree.column("Ngày tổ chức", anchor="center", width=150)

    tree.heading("Giờ bắt đầu", text="Giờ bắt đầu")
    tree.column("Giờ bắt đầu", anchor="center", width=150)

    tree.heading("Giờ kết thúc", text="Giờ kết thúc")
    tree.column("Giờ kết thúc", anchor="center", width=150)

    def block_resize_column(event):
        if tree.identify_region(event.x, event.y) == "separator":
            return "break"

    tree.bind("<Button-1>", block_resize_column)
    tree.bind("<B1-Motion>", block_resize_column)  # Ngăn kéo giãn

    # ========== TÔ MÀU XEN KẼ ==========
    def style_rows():
        for i, item in enumerate(tree.get_children()):
            tree.item(item, tags=("even",) if i % 2 == 0 else ("odd",))
        tree.tag_configure("even", background=TREEVIEW_STYLE["even_row_bg"])
        tree.tag_configure("odd", background=TREEVIEW_STYLE["odd_row_bg"])

    # ========== BUTTON ACTIONS ==========
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
            full_datetime = datetime.strptime(f"{ngay_to_chuc_str} {start_time_str}", "%d/%m/%Y %H:%M:%S")
        except ValueError:
            messagebox.showerror("Lỗi định dạng thời gian",
                                 f"Không thể đọc thời gian hoạt động.\nNgày: {ngay_to_chuc_str}, Giờ: {start_time_str}")
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

    def back_to_main():
        if go_back:
            go_back("main")

    # Button action
    btn_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    btn_frame.pack(fill="x", pady=(0, 15), padx=10)

    #Left frame
    left_frame = tk.Frame(btn_frame, bg=PAGE_BG_COLOR)
    left_frame.pack(side="left", anchor="w")

    btn_back = tk.Button(
        left_frame,
        text="← Quay lại",
        command=back_to_main,
        **BACK_BUTTON_STYLE
    )
    btn_back.pack(side="left")

    #Right frame
    right_frame = tk.Frame(btn_frame, bg=PAGE_BG_COLOR)
    right_frame.pack(side="right", anchor="e")

    btn_edit = tk.Button(
        right_frame,
        text="Sửa hoạt động",
        command=handle_edit,
        **BUTTON_EDIT_STYLE
    )
    btn_edit.pack(side="left", padx=5)

    btn_delete = tk.Button(
        right_frame,
        text="Xóa hoạt động",
        command=handle_delete,
        **BUTTON_DELETE_STYLE
    )
    btn_delete.pack(side="left", padx=5)

    # ========== FUNCTIONS ==========
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

    load_activities()
    style_rows()
