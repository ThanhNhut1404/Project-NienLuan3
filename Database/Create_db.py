import sqlite3

DB_NAME = "Diem_danh.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ---------------- TẠO CÁC BẢNG ------------------

# ADMIN
cursor.execute('''
CREATE TABLE IF NOT EXISTS ADMIN (
    ID_ADMIN INTEGER PRIMARY KEY,
    NAME_ADMIN TEXT,
    PASS_ADMIN TEXT
);
''')

# SINH_VIEN
def create_table_sinh_vien():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SINH_VIEN (
            ID_SV INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME_SV TEXT NOT NULL,
            EMAIL_SV TEXT UNIQUE,
            ADDRESS_SV TEXT,
            DATE_SV DATE,
            SEX_SV INTEGER CHECK (SEX_SV IN (0, 1)),  -- 0: Nam, 1: Nữ
            CLASS_SV TEXT,
            PASSWORD_SV TEXT NOT NULL,
            FACE_ENCODING TEXT,
            CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

# HINH_ANH_KHUON_MAT
cursor.execute('''
CREATE TABLE IF NOT EXISTS HINH_ANH_KHUON_MAT (
    ID_FACE INTEGER PRIMARY KEY,
    FILE_IMG TEXT,
    STATUS TEXT,
    DATE_CREATED TEXT
);
''')

# HK_NK
cursor.execute('''
CREATE TABLE IF NOT EXISTS HK_NK (
    ID_HK INTEGER PRIMARY KEY,
    SCHOOL_YEAR TEXT
);
''')

# HOAT_DONG
cursor.execute('''
CREATE TABLE IF NOT EXISTS HOAT_DONG (
    ID_HD INTEGER PRIMARY KEY,
    TIME_OUT TEXT,
    START_TIME TEXT,
    CATEGORY_HD TEXT
);
''')

# KHOA
cursor.execute('''
CREATE TABLE IF NOT EXISTS KHOA (
    ID_KHOA INTEGER PRIMARY KEY,
    NAME_KHOA TEXT
);
''')

# TAO
cursor.execute('''
CREATE TABLE IF NOT EXISTS TAO (
    ID_HD INTEGER,
    ID_KHOA INTEGER,
    PRIMARY KEY (ID_HD, ID_KHOA),
    FOREIGN KEY (ID_HD) REFERENCES HOAT_DONG(ID_HD),
    FOREIGN KEY (ID_KHOA) REFERENCES KHOA(ID_KHOA)
);
''')

# THAM_GIA
cursor.execute('''
CREATE TABLE IF NOT EXISTS THAM_GIA (
    ID_SV INTEGER,
    ID_HD INTEGER,
    PRIMARY KEY (ID_SV, ID_HD),
    FOREIGN KEY (ID_SV) REFERENCES SINH_VIEN(ID_SV),
    FOREIGN KEY (ID_HD) REFERENCES HOAT_DONG(ID_HD)
);
''')

# DIEM_DANH
cursor.execute('''
CREATE TABLE IF NOT EXISTS DIEM_DANH (
    ID_HD INTEGER,
    ID_FACE INTEGER,
    ID_HK INTEGER,
    PRIMARY KEY (ID_HD, ID_FACE, ID_HK),
    FOREIGN KEY (ID_HD) REFERENCES HOAT_DONG(ID_HD),
    FOREIGN KEY (ID_FACE) REFERENCES HINH_ANH_KHUON_MAT(ID_FACE),
    FOREIGN KEY (ID_HK) REFERENCES HK_NK(ID_HK)
);
''')

conn.commit()
conn.close()

# ----------------- CÁC HÀM XỬ LÝ DỮ LIỆU ------------------

# Thêm sinh viên
def insert_sinh_vien(name, email, address, birthdate, gender, class_sv, password, encoding_json):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO SINH_VIEN (
            NAME_SV, EMAIL_SV, ADDRESS_SV,
            DATE_SV, SEX_SV, CLASS_SV,
            PASSWORD_SV, FACE_ENCODING
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, address, birthdate, gender, class_sv, password, encoding_json))
    conn.commit()
    conn.close()
# Lấy danh sách sinh viên và encoding
def get_all_sinh_vien():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT ID_SV, NAME_SV, FACE_ENCODING FROM SINH_VIEN")
    rows = c.fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1], 'face_encoding': row[2]} for row in rows]

# Kiểm tra sinh viên đã tồn tại
def sinh_vien_exists(name_sv):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM SINH_VIEN WHERE NAME_SV = ?", (name_sv,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Reset bảng SINH_VIEN
def reset_sinh_vien_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS SINH_VIEN")
    conn.commit()
    conn.close()

# Reset và tạo lại bảng SINH_VIEN
def reset_and_create_sinh_vien_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS SINH_VIEN")
    c.execute('''
        CREATE TABLE SINH_VIEN (
            ID_SV INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME_SV TEXT NOT NULL,
            EMAIL_SV TEXT UNIQUE,
            ADDRESS_SV TEXT,
            DATE_SV DATE,
            SEX_SV INTEGER CHECK (SEX_SV IN (0, 1)),
            CLASS_SV TEXT,
            PASSWORD_SV TEXT NOT NULL,
            FACE_ENCODING TEXT,
            CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

print("✅ Tạo cơ sở dữ liệu và các bảng thành công.")
