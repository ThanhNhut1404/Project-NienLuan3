import tkinter as tk
from Student.Styles_student import TITLE_FONT

def render_header(parent, user):
    parent.config(bg="#00897B")
    parent.pack_propagate(0)

    tk.Label(
        parent,
        text="🎓 HỆ THỐNG QUẢN LÝ SINH VIÊN",
        font=TITLE_FONT,
        bg="#00897B",
        fg="white",
        anchor="w",
        padx=20
    ).pack(side="left", fill="y")

    tk.Label(
        parent,
        text=f"Xin chào, {user.get('name', 'Sinh viên')}",
        font=("Arial", 12, "italic"),
        bg="#00897B",
        fg="white",
        anchor="e",
        padx=20
    ).pack(side="right", fill="y")
