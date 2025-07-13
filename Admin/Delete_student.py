import tkinter as tk
from tkinter import ttk, messagebox
from Admin.Styles_admin import LIST_TITLE_FONT, TREEVIEW_STYLE
from Database.Create_db import get_all_sinh_vien, delete_sinh_vien_by_mssv  # Hàm xóa theo MSSV

def render_delete_student(container):
    for widget in container.winfo_children():
        widget.destroy()

    # Style Treeview
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    font=TREEVIEW_STYLE["font"],
                    background="white",
                    foreground="black",
                    rowheight=TREEVIEW_STYLE["rowheight"],
                    fieldbackground="white",
                    bordercolor=TREEVIEW_STYLE["border_color"],
                    borderwidth=1)

    style.configure("Treeview.Heading",
                    font=TREEVIEW_STYLE["header_font"],
                    background=TREEVIEW_STYLE["header_bg"],
                    foreground=TREEVIEW_STYLE["header_fg"])

    style.map("Treeview", background=[("selected", "white")], foreground=[("selected", "black")])
    style.map("Treeview.Heading", background=[("active", TREEVIEW_STYLE["header_bg"])], foreground=[("active", TREEVIEW_STYLE["header_fg"])])
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    tk.Label(container, text="🗑️ Xóa tài khoản sinh viên", font=LIST_TITLE_FONT, bg="white", fg="#990000")\
        .pack(anchor="w", padx=40, pady=(20, 5))

    center_frame = tk.Frame(container, bg="white")
    center_frame.place(relx=0.5, rely=0.5, anchor="n")

    table_frame = tk.Frame(center_frame, bg="white")
    table_frame.pack()

    columns = ("stt", "name", "class", "mssv", "actions")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="none")
    tree.pack(fill=tk.BOTH, expand=True)

    def disable_column_resize(event):
        region = tree.identify_region(event.x, event.y)
        if region == "separator":
            return "break"
    tree.bind("<Button-1>", disable_column_resize)

    tree.heading("stt", text="STT")
    tree.heading("name", text="Họ và Tên")
    tree.heading("class", text="Lớp")
    tree.heading("mssv", text="MSSV")
    tree.heading("actions", text="Chức năng")

    tree.column("stt", width=50, anchor="center", stretch=False)
    tree.column("name", width=250, anchor="w", stretch=False)
    tree.column("class", width=270, anchor="center", stretch=False)
    tree.column("mssv", width=130, anchor="center", stretch=False)
    tree.column("actions", width=200, anchor="center", stretch=False)

    def load_data():
        for row in tree.get_children():
            tree.delete(row)

        students = get_all_sinh_vien()
        for idx, sv in enumerate(students, start=1):
            tag = "even" if idx % 2 == 0 else "odd"
            tree.insert("", "end",
                        values=(idx, sv["name"], sv["class"], sv["mssv"], "❌ Xóa"),
                        tags=(tag,))
        tree.tag_configure("even", background=TREEVIEW_STYLE["even_row_bg"])
        tree.tag_configure("odd", background=TREEVIEW_STYLE["odd_row_bg"])

    def on_tree_click(event):
        region = tree.identify_region(event.x, event.y)
        if region == "cell":
            column = tree.identify_column(event.x)
            row_id = tree.identify_row(event.y)
            if column == "#5" and row_id:  # Cột actions
                values = tree.item(row_id, "values")
                mssv = values[3]
                name = values[1]
                confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sinh viên '{name}'?")
                if confirm:
                    delete_sinh_vien_by_mssv(mssv)
                    load_data()

    tree.bind("<ButtonRelease-1>", on_tree_click)

    load_data()
