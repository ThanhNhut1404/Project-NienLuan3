import tkinter as tk
from tkinter import ttk
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Database.Create_db import DB_NAME

def render_chart_activity(container, user, title=""):
    for widget in container.winfo_children():
        widget.destroy()

    # ===== FRAME BÊN TRÁI =====
    left_frame = tk.Frame(container, bg="#f0f0f0")
    left_frame.pack(side="left", fill="both", expand=False, padx=30, pady=10)

    # ===== TITLE =====
    if title:
        tk.Label(
            left_frame,
            text=title,
            font=("Arial", 14, "bold"),
            fg="#00897B",
            bg="#f0f0f0",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))

    # ===== LẤY TỔNG ĐIỂM HỌC KỲ MỚI NHẤT =====
    tong_diem = 0
    mssv = user.get("mssv")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ID_HK, TONG_DIEM
            FROM TONG_DIEM_HK
            WHERE ID_SV = ?
            ORDER BY ID_HK DESC
            LIMIT 1
        ''', (mssv,))
        result = cursor.fetchone()
        if result:
            tong_diem = result[1]

    diem_con_lai = max(0, 100 - tong_diem)

    # ===== VẼ BIỂU ĐỒ HÌNH TRÒN =====
    labels = ["Đã đạt", "Còn lại"]
    sizes = [tong_diem, diem_con_lai]
    colors = ["#4CAF50", "#B0BEC5"]

    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        textprops={"color": "black", "fontsize": 10}
    )
    ax.axis("equal")

    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10, anchor="w")

    # ===== CHÚ THÍCH TỔNG ĐIỂM =====
    tk.Label(
        left_frame,
        text=f"Tổng điểm học kỳ mới nhất: {tong_diem}/100",
        font=("Arial", 11, "bold"),
        bg="#f0f0f0",
        fg="#333",
        anchor="w"
    ).pack(anchor="w", pady=(0, 10))