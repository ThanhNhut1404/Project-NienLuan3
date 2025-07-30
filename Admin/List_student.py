import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Admin.Styles_admin import LIST_TITLE_FONT, TREEVIEW_STYLE
from Admin.Edit_student import render_student_edit
from Admin.Styles_admin import *
from Database.Create_db import get_all_sinh_vien, delete_sinh_vien_by_mssv  # Đảm bảo hàm này trả về list[dict]

def on_tree_click(event, tree, container):
    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return

    row_id = tree.identify_row(event.y)
    column = tree.identify_column(event.x)

    if not row_id or column != "#5":
        return

    item = tree.item(row_id)
    values = item["values"]
    if not values:
        return

    mssv = str(values[3]).strip()  # MSSV ở cột thứ 4
    name = values[1]

    bbox = tree.bbox(row_id, column)
    if not bbox:
        return

    click_offset = event.x - bbox[0]

    sửa_text = "🛠 Sửa"
    xóa_text = "❌ Xóa"

    font = ("Arial", 11)
    temp = tk.Label(tree, text=sửa_text, font=font)
    temp.update_idletasks()
    sửa_width = temp.winfo_reqwidth()

    temp.config(text=" | ")
    temp.update_idletasks()
    separator_width = temp.winfo_reqwidth()

    temp.config(text=xóa_text)
    temp.update_idletasks()
    xóa_width = temp.winfo_reqwidth()

    del temp

    if click_offset <= sửa_width:
        students = get_all_sinh_vien()
        selected_sv = next((sv for sv in students if sv["mssv"] == mssv), None)
        if selected_sv:
            render_student_edit(container, selected_sv)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu sinh viên.")
    elif click_offset >= sửa_width + separator_width:
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sinh viên: {name} ({mssv})?")
        if confirm:
            delete_sinh_vien_by_mssv(mssv)
            tree.delete(row_id)
            for idx, item_id in enumerate(tree.get_children(), start=1):
                item_vals = list(tree.item(item_id)["values"])
                item_vals[0] = idx
                tree.item(item_id, values=item_vals)
            messagebox.showinfo("Thành công", f"Đã xóa sinh viên '{name}' khỏi hệ thống.")

def render_student_list(container):
    for widget in container.winfo_children():
        widget.destroy()

    selected_row = {"item_id": None}

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

    style.map("Treeview",
              background=[("selected", "white")],
              foreground=[("selected", "black")])

    style.configure("Treeview.Heading",
                    font=TREEVIEW_STYLE["header_font"],
                    background=TREEVIEW_STYLE["header_bg"],
                    foreground=TREEVIEW_STYLE["header_fg"])

    style.map("Treeview.Heading",
              background=[("active", TREEVIEW_STYLE["header_bg"])],
              foreground=[("active", TREEVIEW_STYLE["header_fg"])])

    style.layout("Treeview", [
        ('Treeview.treearea', {'sticky': 'nswe'})
    ])

    header_frame = tk.Frame(container, bg="white")
    header_frame.pack(fill="x", padx=40, pady=(20, 5))

    tk.Label(header_frame, text="📋 Danh sách sinh viên", font=LIST_TITLE_FONT, bg="white", fg="#003366") \
        .pack(side="left")

    search_frame = tk.Frame(header_frame, bg="white")
    search_frame.pack(side="right")

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 11), width=30)
    search_entry.pack(side="left", padx=(0, 10))

    def perform_search():
        keyword = search_var.get().lower().strip()
        filtered_students = []
        for sv in get_all_sinh_vien():
            if (keyword in sv["name"].lower()
                    or keyword in sv["class"].lower()
                    or keyword in sv["mssv"].lower()):
                filtered_students.append(sv)

        tree.delete(*tree.get_children())
        for idx, sv in enumerate(filtered_students, start=1):
            tag = "even" if idx % 2 == 0 else "odd"
            tree.insert("", "end", values=(idx, sv["name"], sv["class"], sv["mssv"], "🛠 Sửa | ❌ Xóa"), tags=(tag,))

    search_btn = tk.Button(search_frame, text="Tìm kiếm", command=perform_search, **BUTTON_SHEARCH_STYLE)
    search_btn.pack(side="left")

    center_frame = tk.Frame(container, bg="white")
    center_frame.pack(pady=(0, 20))

    table_frame = tk.Frame(center_frame, bg="white")
    table_frame.pack()

    columns = ("stt", "name", "class", "mssv", "actions")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="none")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.tag_configure("even", background=TREEVIEW_STYLE["even_row_bg"])
    tree.tag_configure("odd", background=TREEVIEW_STYLE["odd_row_bg"])
    tree.tag_configure("selected_highlight", background="#DDEEFF")

    def handle_click_with_highlight(event, container):
        region = tree.identify_region(event.x, event.y)
        if region == "separator":
            return "break"

        row_id = tree.identify_row(event.y)
        if not row_id:
            return

        if selected_row["item_id"] and tree.exists(selected_row["item_id"]):
            idx = tree.index(selected_row["item_id"])
            tag = "even" if (idx + 1) % 2 == 0 else "odd"
            tree.item(selected_row["item_id"], tags=(tag,))

        current_tags = tree.item(row_id)["tags"]
        new_tags = tuple(t for t in current_tags if t != "selected_highlight") + ("selected_highlight",)
        tree.item(row_id, tags=new_tags)
        selected_row["item_id"] = row_id

        on_tree_click(event, tree, container)

    tree.bind("<Button-1>", lambda e: handle_click_with_highlight(e, container))

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

    students = get_all_sinh_vien()
    for idx, sv in enumerate(students, start=1):
        tag = "even" if idx % 2 == 0 else "odd"
        tree.insert("", "end", values=(idx, sv["name"], sv["class"], sv["mssv"], "🛠 Sửa | ❌ Xóa"), tags=(tag,))
