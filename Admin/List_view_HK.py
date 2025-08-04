import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from Admin.Styles_admin import *
from Admin.Edit_HK import render_edit_hk  # <- Thêm import hàm edit học kỳ

DB_NAME = "Database/Diem_danh.db"

def render_list_view_hk(container, go_back):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg=PAGE_BG_COLOR)

    wrapper = tk.Frame(container, bg=PAGE_BG_COLOR)
    wrapper.pack(fill=tk.BOTH, expand=True)

    title_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    title_frame.pack(fill="x", padx=20, pady=(20, 5))

    tk.Label(title_frame, text="📅 Danh sách học kỳ", font=TITLE_FONT, bg="white", fg="#003366") \
        .pack(side="left")

    def perform_search():
        keyword = search_var.get().lower().strip()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT NAME_HK, SCHOOL_YEAR FROM HK_NK")
        rows = cursor.fetchall()
        conn.close()

        tree.delete(*tree.get_children())
        for index, row in enumerate(rows, start=1):
            if keyword in row[0].lower():
                tree.insert("", "end", values=(index, row[0], row[1]))
        style_rows()

    search_wrapper = tk.Frame(title_frame, bg=PAGE_BG_COLOR)
    search_wrapper.pack(side="right")

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_wrapper, textvariable=search_var, font=("Arial", 11), width=30, bg="#f8f8f8")
    search_entry.pack(side="left", padx=(0, 6))

    search_btn = tk.Button(search_wrapper, text="Tìm kiếm", command=perform_search, **BUTTON_SHEARCH_STYLE)
    search_btn.pack(side="left")

    tree_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 5))

    style = ttk.Style()
    style.theme_use("default")
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
    style.configure("Treeview", font=TREEVIEW_STYLE["font"], rowheight=TREEVIEW_STYLE["rowheight"],
                    background="white", foreground="black", fieldbackground="white")
    style.configure("Treeview.Heading", font=TREEVIEW_STYLE["header_font"],
                    background=TREEVIEW_STYLE["header_bg"], foreground=TREEVIEW_STYLE["header_fg"])
    style.map("Treeview.Heading", background=[("active", TREEVIEW_STYLE["header_bg"])])

    columns = ("STT", "Tên học kỳ", "Niên khóa")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("STT", text="STT")
    tree.column("STT", anchor="center", width=10)
    tree.heading("Tên học kỳ", text="Tên học kỳ")
    tree.column("Tên học kỳ", anchor="w", width=250)
    tree.heading("Niên khóa", text="Niên khóa")
    tree.column("Niên khóa", anchor="center", width=150)

    def block_resize_column(event):
        if tree.identify_region(event.x, event.y) == "separator":
            return "break"
    tree.bind("<Button-1>", block_resize_column)
    tree.bind("<B1-Motion>", block_resize_column)

    def style_rows():
        for i, item in enumerate(tree.get_children()):
            tree.item(item, tags=("even",) if i % 2 == 0 else ("odd",))
        tree.tag_configure("even", background=TREEVIEW_STYLE["even_row_bg"])
        tree.tag_configure("odd", background=TREEVIEW_STYLE["odd_row_bg"])

    def handle_edit():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một học kỳ để sửa.")
            return

        selected_values = tree.item(selected_item, 'values')
        if not selected_values or len(selected_values) < 3:
            messagebox.showerror("Lỗi", "Dữ liệu học kỳ không đầy đủ.")
            return

        name_hk = selected_values[1]
        school_year = selected_values[2]

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM HK_NK WHERE NAME_HK = ? AND SCHOOL_YEAR = ?", (name_hk, school_year))
            result = cursor.fetchone()
            conn.close()

            if not result:
                messagebox.showerror("Lỗi", "Không tìm thấy học kỳ để sửa.")
                return

            # Gọi hàm chỉnh sửa và truyền đầy đủ dữ liệu học kỳ
            from Admin.Edit_HK import render_edit_hk
            render_edit_hk(container, result, lambda: render_list_view_hk(container, go_back))


        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Đã xảy ra lỗi khi tìm học kỳ: {e}")

    def handle_delete():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một học kỳ để xóa.")
            return

        selected_values = tree.item(selected_item, 'values')
        if not selected_values:
            return

        name_hk = selected_values[1]
        school_year = selected_values[2]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT ID_HK FROM HK_NK WHERE NAME_HK = ? AND SCHOOL_YEAR = ?", (name_hk, school_year))
        result = cursor.fetchone()
        if not result:
            conn.close()
            messagebox.showerror("Lỗi", "Không tìm thấy học kỳ để xóa.")
            return

        id_hk = result[0]

        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa học kỳ này?")
        if confirm:
            cursor.execute("DELETE FROM HK_NK WHERE ID_HK = ?", (id_hk,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Đã xóa học kỳ.")
            load_hk()

    def back_to_main():
        if go_back:
            go_back("main")

    btn_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    btn_frame.pack(fill="x", pady=(0, 15), padx=10)

    left_frame = tk.Frame(btn_frame, bg=PAGE_BG_COLOR)
    left_frame.pack(side="left", anchor="w")
    btn_back = tk.Button(left_frame, text="← Quay lại", command=back_to_main, **BACK_BUTTON_STYLE)
    btn_back.pack(side="left")

    right_frame = tk.Frame(btn_frame, bg=PAGE_BG_COLOR)
    right_frame.pack(side="right", anchor="e")

    btn_delete = tk.Button(right_frame, text="Xóa học kỳ", command=handle_delete, **BUTTON_DELETE_HK_STYLE)
    btn_delete.pack(side="left", padx=5)

    btn_edit = tk.Button(right_frame, text="Sửa học kỳ", command=handle_edit, **BUTTON_EDIT_STYLE)
    btn_edit.pack(side="left", padx=5)

    def load_hk():
        tree.delete(*tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT NAME_HK, SCHOOL_YEAR FROM HK_NK")
        rows = cursor.fetchall()
        conn.close()

        for index, row in enumerate(rows, start=1):
            tree.insert("", "end", values=(index, row[0], row[1]))
        style_rows()

    load_hk()
