# Kích thước cửa sổ nếu cần
APP_SIZE = "980x720"

# ==== Màu nền ====
PAGE_BG_COLOR = "white"        # Màu nền tổng thể
FORM_BG_COLOR = "#003366"        # Màu nền form đăng ký

# ==== Viền và định dạng form ====
FORM_BORDER_WIDTH = 2
FORM_BORDER_STYLE = "groove"

#Khung nhập liệu
FORM_WIDTH = 480
FORM_HEIGHT = 600


# ==== Font ====
TITLE_FONT = ("Arial", 17, "bold")      # Tiêu đề lớn
LABEL_FONT = ("Arial", 15, "bold")      # Nhãn label
ENTRY_FONT = ("Arial", 13)
CAMERA_NOTE_FONT = ("Arial", 11, "italic")
COUNTER_FONT = ("Arial", 14, "bold")
ERROR_FONT = ("Arial", 10, "italic")
LIST_TITLE_FONT = ("Arial", 17, "bold")  # Tiêu đề danh sách

# ==== Màu thông báo lỗi ====
ERROR_FG = "red"

# ==== Padding chung ====
FORM_PADDING_X = 20
FORM_PADDING_Y = 15

# ==== Padding riêng ====
FORM_LABEL_PADX = 15         # Lề trái của Label
FORM_ENTRY_PADX = 5         # Lề trái của Entry
FORM_CHECKBOX_PADX = 18      # Lề trái của Checkbutton
FORM_BUTTON_PADY = 20        # Khoảng cách dưới nút Đăng nhập

# ==== Style cho nút chính ====
BUTTON_STYLE = {
    "font": ("Arial", 14, "bold"),
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#388E3C",
    "bd": 2,
    "relief": "raised",
    "width": 10,
    "height": 1
}

#Sửa hoạt động
BUTTON_EDIT_STYLE = {
    "font": ("Arial", 14, "bold"),
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#388E3C",
    "bd": 2,
    "relief": "raised",
    "width": 13,
    "height": 1
}

#Tìm kiếm
BUTTON_SHEARCH_STYLE = {
    "font": ("Arial", 9, "bold"),
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#388E3C",
    "bd": 2,
    "relief": "raised",
    "width": 9,
    "height": 1
}

#Xem danh sách tham hoạt động
BUTTON_VIEW_STYLE = {
    "font": ("Arial", 14, "bold"),
    "bg": "#07A8A3",
    "fg": "white",
    "activebackground": "#388E3C",
    "bd": 2,
    "relief": "raised",
    "width": 23,
    "height": 1
}

BUTTON_DELETE_STYLE = {
    "font": ("Arial", 14, "bold"),
    "bg": "#FFA726",
    "fg": "white",
    "activebackground": "#FF5722",
    "bd": 2,
    "relief": "raised",
    "width": 13,
    "height": 1
}

BUTTON_DELETE_HK_STYLE= {
    "font": ("Arial", 14, "bold"),
    "bg": "#FFA726",
    "fg": "white",
    "activebackground": "#FF5722",
    "bd": 2,
    "relief": "raised",
    "width": 9,
    "height": 1
}

# ==== Style cho checkbox hiện mật khẩu ====
CHECKBOX_STYLE = {
    "bg": FORM_BG_COLOR,
    "fg": "white",
    "activebackground": FORM_BG_COLOR,
    "activeforeground": "white",
    "selectcolor": "white",
    "font": ("Arial", 10, "bold")
}

#Style cho nút menu (Header_admin)
MENU_BUTTON_STYLE = {
    "font": ("Arial", 11, "bold"),
    "bg": "#003366",
    "fg": "white",
    "activebackground": "#005599",
    "activeforeground": "white",
    "bd": 0,
    "padx": 12,
    "pady": 7
}

#Style cho separator dọc giữa các menu
SEPARATOR_STYLE = {
    "bg": "#BDC3C7",
    "width": 1,
    "height": 30
}

# ==== Ghi chú camera (Create_student)
CAMERA_NOTE = (
    'Camera sẽ bắt đầu chụp sau khi nhấn "Tạo tài khoản".\n'
    'Hệ thống sẽ chụp 5 ảnh khuôn mặt. Hãy nhìn thẳng vào camera.'
)

# Nút "Tạo tài khoản"
CREATE_BUTTON_STYLE = {
    "font": ("Arial", 14, "bold"),
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#388E3C",
    "bd": 2,
    "relief": "raised",
    "width": 12,
    "height": 1
}

# Nút tạo hoạt động
CREATE_BUTTON_STYLE = {
    "font": ("Arial", 14, "bold"),
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#388E3C",
    "bd": 2,
    "relief": "raised",
    "width": 12,
    "height": 1
}

# Nút "← Quay lại"
BACK_BUTTON_STYLE = {
    "font": ("Arial", 13, "bold"),
    "bg": "#f44336",
    "fg": "white",
    "activebackground": "#d32f2f",
    "bd": 2,
    "relief": "raised",
    "width": 10,
    "height": 1
}

# Nút cập nhật trong list_view_activity
SAVE_BUTTON_STYLE = {
    "bg": "#2196f3",
    "fg": "white",
    "font": ("Arial", 10, "bold"),
    "activebackground": "#1976d2",
    "activeforeground": "white",
    "bd": 2,
    "relief": "raised",
    "width": 15
}

# Checkbox "Hiện mật khẩu"
CHECKBOX_STYLE = {
    "bg": FORM_BG_COLOR,
    "fg": "white",
    "activebackground": FORM_BG_COLOR,
    "activeforeground": "white",
    "selectcolor": "black",
    "font": ("Arial", 10, "bold")
}



# Nút "OK" trong popup thông báo
POPUP_OK_BUTTON_STYLE = {
    "font": ("Arial", 12, "bold"),
    "bg": "#f44336",
    "fg": "white",
    "activebackground": "#c62828",
    "bd": 0,
    "relief": "flat",
    "width": 10,
    "height": 1
}


#Bảng danh sách
TREEVIEW_STYLE = {
    "font": ("Arial", 14),     # Cỡ chữ trong bảng
    "rowheight": 29,            # Chiều cao mỗi dòng
    "header_font": ("Arial", 16, "bold"),  # Tiêu đề bảng
    "header_bg": "#003366",
    "header_fg": "white",
    "even_row_bg": "#f2f2f2",
    "odd_row_bg": "white",
    "border_color": "#d9d9d9"
}

# Create_ativity
ENTRY_STYLE_ACTIVITY = {
    "font": ENTRY_FONT,
    "bg": "white",
    "fg": "black",
    "width": 25
}


COMBOBOX_STYLE = {
    "font": ENTRY_FONT,
    "width": 25,
    "state": "readonly"
}


DATE_ENTRY_STYLE = {
    "width": 29,
    "date_pattern": "dd/mm/yyyy",
    "background": "darkblue",
    "foreground": "white",
    "font": ("Arial", 10)
}


SPINBOX_STYLE = {
    "from_": 0,
    "to": 59,
    "width": 5,
    "format": "%02.0f",
    "font": ("Arial", 10)
}

RADIO_STYLE = {
    "bg": FORM_BG_COLOR,
    "font": ("Arial", 10)
}
