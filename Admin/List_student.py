import tkinter as tk
from tkinter import ttk, messagebox
from Admin.Styles_admin import *
from Admin.Edit_student import render_student_edit
from Database.Create_db import get_all_sinh_vien, delete_sinh_vien_by_mssv



def render_student_list(container, go_back):
    # Clear container
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg=PAGE_BG_COLOR)

    # MAIN WRAPPER
    wrapper = tk.Frame(container, bg=PAGE_BG_COLOR)
    wrapper.pack(fill=tk.BOTH, expand=True)

    # TITLE + SEARCH
    title_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    title_frame.pack(fill="x", padx=20, pady=(20, 5))  # KHỚP VỚI tree_frame (padx=20)

    # Tiêu đề bên trái
    tk.Label(title_frame, text="📋 Danh sách sinh viên", font=TITLE_FONT, bg="white", fg="#003366").pack(side="left",
                                                                                                        anchor="w")

    # Tìm kiếm bên phải
    search_wrapper = tk.Frame(title_frame, bg=PAGE_BG_COLOR)
    search_wrapper.pack(side="right", anchor="e")  # Gắn sát phải, trong cùng mép treeview

    search_var = tk.StringVar()
    tk.Entry(search_wrapper, textvariable=search_var, font=("Arial", 11), width=30, bg="#f8f8f8").pack(side="left", padx=(0, 6))
    tk.Button(search_wrapper, text="Tìm kiếm", command=lambda: perform_search(), **BUTTON_SHEARCH_STYLE).pack(
        side="left")
    # TREEVIEW
    tree_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10,5))

    style = ttk.Style()
    style.theme_use("default")
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
    style.configure("Treeview", font=TREEVIEW_STYLE["font"], rowheight=TREEVIEW_STYLE["rowheight"],
                    background="white", foreground="black", fieldbackground="white")
    style.configure("Treeview.Heading", font=TREEVIEW_STYLE["header_font"],
                    background=TREEVIEW_STYLE["header_bg"], foreground=TREEVIEW_STYLE["header_fg"])
    style.map("Treeview.Heading", background=[("active", TREEVIEW_STYLE["header_bg"])])

    columns = ("stt", "name", "class", "mssv", "date")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
    tree.pack(fill=tk.BOTH, expand=True)

    # Headings
    tree.heading("stt", text="STT")
    tree.column("stt", anchor="center", width=50)
    tree.heading("name", text="Họ và Tên")
    tree.column("name", anchor="w", width=260)
    tree.heading("class", text="Lớp")
    tree.column("class", anchor="center", width=300)
    tree.heading("mssv", text="MSSV")
    tree.column("mssv", anchor="center", width=130)
    tree.heading("date", text="Ngày sinh")
    tree.column("date", anchor="center", width=160)

    tree.tag_configure("even", background=TREEVIEW_STYLE["even_row_bg"])
    tree.tag_configure("odd", background=TREEVIEW_STYLE["odd_row_bg"])

    tree.bind("<Button-1>", lambda e: block_resize_column(e, tree))

    def back_to_main():
        if go_back:
            go_back("main")

    # BUTTONS FRAME
    btn_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    btn_frame.pack(fill="x", pady=(0,15), padx=10)

    left_frame = tk.Frame(btn_frame, bg=PAGE_BG_COLOR)
    left_frame.pack(side="left", anchor="w")

    btn_back = tk.Button(left_frame, text="← Quay lại", command=back_to_main, **BACK_BUTTON_STYLE)
    btn_back.pack(side="left")

    right_frame = tk.Frame(btn_frame, bg=PAGE_BG_COLOR)
    right_frame.pack(side="right", anchor="e")

    tk.Button(right_frame, text="Xóa sinh viên", command=lambda: handle_delete(tree, container), **BUTTON_DELETE_STYLE).pack(side="left", padx=5)
    tk.Button(right_frame, text="Sửa thông tin", command=lambda: handle_edit(tree, container), **BUTTON_EDIT_STYLE).pack(side="left", padx=5)

    # Local functions
    def perform_search():
        keyword = search_var.get().lower().strip()
        filtered = [sv for sv in get_all_sinh_vien() if keyword in sv["name"].lower() or keyword in sv["class"].lower() or keyword in sv["mssv"].lower()]
        tree.delete(*tree.get_children())
        for idx, sv in enumerate(filtered, start=1):
            tag = "even" if idx%2==0 else "odd"
            tree.insert("", "end", values=(idx, sv["name"], sv["class"], sv["mssv"], sv["date"]), tags=(tag,))

    def load_students():
        tree.delete(*tree.get_children())
        students = get_all_sinh_vien()
        for idx, sv in enumerate(students, start=1):
            tag = "even" if idx%2==0 else "odd"
            tree.insert("", "end", values=(idx, sv["name"], sv["class"], sv["mssv"], sv["date"]), tags=(tag,))

    def get_selected():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sinh viên.")
            return None
        return tree.item(sel, "values")

    def handle_edit(treeview, container_frame):
        vals = get_selected()
        if not vals: return
        mssv = vals[3]
        sv = next((s for s in get_all_sinh_vien() if s["mssv"]==mssv), None)
        if sv: render_student_edit(container_frame, sv)

    def handle_delete(treeview, container_frame):
        vals = get_selected()
        if not vals: return
        mssv, name = vals[3], vals[1]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sinh viên {name}?"):
            delete_sinh_vien_by_mssv(mssv)
            load_students()

    def block_resize_column(event, treeview):
        if treeview.identify_region(event.x, event.y)=="separator":
            return "break"

    # Load initial data
    load_students()
