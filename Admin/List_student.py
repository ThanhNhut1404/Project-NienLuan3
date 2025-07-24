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

    mssv = str(values[3]) .strip()  # MSSV ở cột thứ 4
    name = values[1]

    bbox = tree.bbox(row_id, column)
    if not bbox:
        return

    click_offset = event.x - bbox[0]

    # Dự đoán chiều rộng từng phần bằng pixel tương đối
    sửa_text = "🛠 Sửa"
    xóa_text = "❌ Xóa"

    font = ("Arial", 11)  # hoặc dùng font bạn set trong TREEVIEW_STYLE["font"]
    temp = tk.Label(tree, text=sửa_text, font=font)
    temp.update_idletasks()
    sửa_width = temp.winfo_reqwidth()

    temp.config(text=" | ")
    temp.update_idletasks()
    separator_width = temp.winfo_reqwidth()

    temp.config(text=xóa_text)
    temp.update_idletasks()
    xóa_width = temp.winfo_reqwidth()

    del temp  # cleanup

    # Phân vùng click
    if click_offset <= sửa_width:
        # ====== BẤM SỬA ======
        students = get_all_sinh_vien()
        selected_sv = next((sv for sv in students if sv["mssv"] == mssv), None)
        if selected_sv:
            render_student_edit(container, selected_sv)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu sinh viên.")
    elif click_offset >= sửa_width + separator_width:
        # ====== BẤM XÓA ======
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sinh viên: {name} ({mssv})?")
        if confirm:
            delete_sinh_vien_by_mssv(mssv)
            tree.delete(row_id)
            # Cập nhật lại STT
            for idx, item_id in enumerate(tree.get_children(), start=1):
                item_vals = list(tree.item(item_id)["values"])
                item_vals[0] = idx
                tree.item(item_id, values=item_vals)
            messagebox.showinfo("Thành công", f"Đã xóa sinh viên '{name}' khỏi hệ thống.")

def render_student_list(container):
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
                    borderwidth=1
                    )

    style.map("Treeview",
              background=[("selected", "white")],
              foreground=[("selected", "black")]
              )

    style.configure("Treeview.Heading",
                    font=TREEVIEW_STYLE["header_font"],
                    background=TREEVIEW_STYLE["header_bg"],
                    foreground=TREEVIEW_STYLE["header_fg"]
                    )

    style.map("Treeview.Heading",
              background=[("active", TREEVIEW_STYLE["header_bg"])],
              foreground=[("active", TREEVIEW_STYLE["header_fg"])]
              )

    style.layout("Treeview", [
        ('Treeview.treearea', {'sticky': 'nswe'})
    ])

    # Tiêu đề căn trái
    tk.Label(container, text="📋 Danh sách sinh viên", font=LIST_TITLE_FONT, bg="white", fg="#003366") \
        .pack(anchor="w", padx=40, pady=(20, 5))  # Căn lề trái, cách lề 40px

    # Bảng Treeview nằm giữa
    center_frame = tk.Frame(container, bg="white")
    center_frame.pack(pady=(0, 20))

    table_frame = tk.Frame(center_frame, bg="white")
    table_frame.pack()

    columns = ("stt", "name", "class", "mssv", "actions")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="none")
    tree.pack(fill=tk.BOTH, expand=True)

    # Kết hợp cả: ngăn kéo cột + xử lý click nút "Xóa"
    def handle_click(event, container):
        region = tree.identify_region(event.x, event.y)
        if region == "separator":
            return "break"
        on_tree_click(event, tree, container)

    tree.bind("<Button-1>", lambda e: handle_click(e, container))


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

    # Load dữ liệu sinh viên
    students = get_all_sinh_vien()
    for idx, sv in enumerate(students, start=1):
        tag = "even" if idx % 2 == 0 else "odd"
        tree.insert(
            "", "end",
            values=(idx, sv["name"], sv["class"], sv["mssv"], "🛠 Sửa | ❌ Xóa"),
            tags=(tag,)
        )

    # Cấu hình màu xen kẽ cho từng dòng
    tree.tag_configure("even", background=TREEVIEW_STYLE["even_row_bg"])
    tree.tag_configure("odd", background=TREEVIEW_STYLE["odd_row_bg"])




