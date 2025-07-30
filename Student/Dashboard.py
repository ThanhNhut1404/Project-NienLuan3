import tkinter as tk
from Student.View_infor import render_view_infor
from Student.Chart_activity import render_chart_activity

def render_dashboard(container, user):
    for widget in container.winfo_children():
        widget.destroy()
    container.config(bg="#f0f0f0")

    # ===== Thông tin sinh viên =====
    render_view_infor(container, user)

    # ===== Biểu đồ rèn luyện học kỳ =====
    chart_frame = tk.Frame(container, bg="#f0f0f0")
    chart_frame.pack(fill="x", pady=(10, 20))
    render_chart_activity(chart_frame, user, title="📊 Tiến độ điểm rèn luyện học kỳ hiện tại")
