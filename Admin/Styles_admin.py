# Kích thước cửa sổ nếu cần dùng cho Admin_app.py
APP_SIZE = "980x620"

# ==== Font ====
TITLE_FONT = ("Arial", 20, "bold")
LABEL_FONT = ("Arial", 18, "bold")
ENTRY_FONT = ("Arial", 13)

# ==== Style cho Button chính ====
BUTTON_STYLE = {
    "font": ("Arial", 15, "bold"),
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#388E3C",
    "bd": 0,
    "relief": "flat",
    "width": 10,
    "height": 1
}

# ==== Style cho nút menu ====
MENU_BUTTON_STYLE = {
    "font": ("Arial", 11, "bold"),
    "bg": "#003366",
    "fg": "white",
    "activebackground": "#005599",  # Hover tối hơn 1 chút
    "activeforeground": "white",
    "bd": 0,
    "padx": 12,
    "pady": 7
}

# ==== Style cho separator phân cách dọc giữa các menu ====
SEPARATOR_STYLE = {
    "bg": "#BDC3C7",
    "width": 1,
    "height": 30
}

# ==== Style cho form đăng nhập (ô vuông trắng) ====
FORM_BG_COLOR = "white"
FORM_BORDER_WIDTH = 2
FORM_BORDER_STYLE = "groove"
FORM_PADDING_Y = 20  # Padding top cho toàn bộ form (khoảng cách dòng đầu tiên)

# ✅ Padding riêng cho từng phần trong form (tùy chỉnh độc lập)
FORM_LABEL_PADX = 15         # Lề trái của Label
FORM_ENTRY_PADX = 20         # Lề trái của Entry
FORM_CHECKBOX_PADX = 18      # Lề trái của Checkbutton
FORM_BUTTON_PADY = 20        # Khoảng cách dưới nút Đăng nhập

# ==== Style cho checkbox hiện mật khẩu ====
CHECKBOX_STYLE = {
    "bg": FORM_BG_COLOR,
    "fg": "black",
    "activebackground": FORM_BG_COLOR,
    "activeforeground": "black",
    "selectcolor": FORM_BG_COLOR,
    "font": ("Arial", 10)
}
