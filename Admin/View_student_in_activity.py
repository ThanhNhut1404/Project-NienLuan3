import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from Admin.Styles_admin import *
from Database.Create_db import DB_NAME
from datetime import datetime
from tkinter import filedialog


def render_student_in_activity(container, id_hoat_dong, go_back):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg=PAGE_BG_COLOR)

    # Truy vấn tên hoạt động
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT TEN_HD FROM HOAT_DONG WHERE ID_HD = ?", (id_hoat_dong,))
    result = cursor.fetchone()
    ten_hd = result[0] if result else "Không rõ"
    conn.close()

    # ========== MAIN WRAPPER ==========
    wrapper = tk.Frame(container, bg=PAGE_BG_COLOR)
    wrapper.pack(fill=tk.BOTH, expand=True)

    # ========== TITLE ==========
    title_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    title_frame.pack(anchor="w", padx=28, pady=(20, 5))
    tk.Label(
        title_frame,
        text=f"📃 Danh sách sinh viên tham gia hoạt động \"{ten_hd}\"",
        font=TITLE_FONT,
        bg="white",
        fg="#003366"
    ).pack(anchor="w")

    tree_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    tree_frame.pack(fill="both", expand=True, padx=20)

    columns = ("STT", "Họ tên", "Lớp", "MSSV", "Thời gian")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    # Thiết lập heading và độ rộng từng cột (tối ưu hiển thị)
    tree.heading("STT", text="STT")
    tree.column("STT", anchor="center", width=50, stretch=False)  # Vừa đủ cho 2 chữ số

    tree.heading("Họ tên", text="Họ tên")
    tree.column("Họ tên", anchor="w", width=260, stretch=False)  # Đủ cho tên dài

    tree.heading("Lớp", text="Lớp")
    tree.column("Lớp", anchor="center", width=287, stretch=False)

    tree.heading("MSSV", text="MSSV")
    tree.column("MSSV", anchor="center", width=120, stretch=False)  # Thường 9-10 ký tự

    tree.heading("Thời gian", text="Thời gian")
    tree.column("Thời gian", anchor="center", width=215, stretch=False)  # Có thể giãn nếu dư chỗ

    tree.pack(fill="both", expand=True)

    # Ngăn không cho kéo giãn các cột
    def block_resize_column(event):
        if tree.identify_region(event.x, event.y) == "separator":
            return "break"

    tree.bind("<Button-1>", block_resize_column)
    tree.bind("<B1-Motion>", block_resize_column)

    style = ttk.Style()
    style.configure("Treeview", **TREEVIEW_STYLE)

    # Truy vấn dữ liệu
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sv.NAME_SV, sv.CLASS_SV, sv.MSSV, dd.thoi_gian
        FROM DIEM_DANH_HOAT_DONG dd
        JOIN SINH_VIEN sv ON sv.MSSV = dd.MSSV
        WHERE dd.id_hoat_dong = ?
    ''', (id_hoat_dong,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showinfo("Thông báo", "Chưa có sinh viên nào tham gia hoạt động này.")
    else:
        for index, row in enumerate(records, start=1):
            name, lop, mssv, thoi_gian = row

            try:
                # tách chuỗi datetime -> giờ + ngày
                dt = datetime.strptime(thoi_gian, "%Y-%m-%d %H:%M:%S")
                gio = dt.strftime("%H:%M:%S")
                ngay = dt.strftime("%d/%m/%Y")
            except:
                gio = "??:??"
                ngay = "??/??/????"

            thoigian_hien_thi = f"{gio} - {ngay}"
            tree.insert("", "end", values=(index, name, lop, mssv, thoigian_hien_thi))

    # Nút quay lại
    def back_to_main():
        if go_back:
            go_back()

    wrapper = tk.Frame(container, bg=PAGE_BG_COLOR)
    wrapper.pack(fill="x")

    btn_frame = tk.Frame(wrapper, bg=PAGE_BG_COLOR)
    btn_frame.pack(fill="x", pady=(0, 15), padx=10)

    left_frame = tk.Frame(btn_frame, bg=PAGE_BG_COLOR)
    left_frame.pack(side="left", anchor="w")

    btn_back = tk.Button(
        left_frame,
        text="← Quay lại",
        command=back_to_main,
        **BACK_BUTTON_STYLE
    )
    btn_back.pack(side="left")

    btn_back.pack(side="left")

    # Nút in danh sách
    def export_pdf():
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from tkinter import filedialog
        import os

        font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
        pdfmetrics.registerFont(TTFont("DejaVu", font_path))

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Danh sách {ten_hd}.pdf".replace(" ", "_"),
            title="Lưu file danh sách"
        )
        if not file_path:
            return  # Người dùng hủy

        doc = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        title = Paragraph(f'<font name="DejaVu">Danh sách sinh viên tham gia hoạt động "{ten_hd}"</font>', styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        table_data = [["STT", "Họ tên", "Lớp", "MSSV", "Thời gian"]]
        for child in tree.get_children():
            table_data.append(tree.item(child)["values"])

        table = Table(table_data, colWidths=[40, 150, 170, 70, 130])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C387E")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVu'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ]))
        elements.append(table)

        doc.build(elements)
        messagebox.showinfo("Thành công", f"Đã lưu file: {file_path}")


    # Nút in nằm bên phải
    right_frame = tk.Frame(btn_frame, bg=PAGE_BG_COLOR)
    right_frame.pack(side="right", anchor="e")

    btn_export = tk.Button(
        right_frame,
        text="🖨 In danh sách",
        command=export_pdf,
        **BUTTON_EDIT_STYLE
    )
    btn_export.pack(side="right")

