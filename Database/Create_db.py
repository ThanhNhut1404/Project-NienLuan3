import os
import json
import sqlite3



# ✅ Luôn đảm bảo file .db nằm trong thư mục Database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "Diem_danh.db")

# ================== KẾT NỐI DB =====================
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

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
cursor.execute('''
CREATE TABLE IF NOT EXISTS SINH_VIEN (
    ID_SV INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME_SV TEXT NOT NULL,
    MSSV TEXT UNIQUE,
    EMAIL_SV TEXT UNIQUE,
    ADDRESS_SV TEXT,
    DATE_SV DATE,
    SEX_SV INTEGER CHECK (SEX_SV IN (0, 1)),
    CLASS_SV TEXT,
    PHONE_SV TEXT, 
    PASSWORD_SV TEXT NOT NULL,
    TONG_DIEM_HD INTEGER DEFAULT 0,
    FACE_ENCODING TEXT,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

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
    NAME_HK TEXT NOT NULL,           -- Tên học kỳ
    SCHOOL_YEAR TEXT
);
''')

# HOAT_DONG
cursor.execute('''
CREATE TABLE IF NOT EXISTS HOAT_DONG (
    ID_HD INTEGER PRIMARY KEY AUTOINCREMENT,
    TEN_HD TEXT NOT NULL,           -- Tên hoạt động
    CATEGORY_HD TEXT,               -- Loại hoạt động: Tình nguyện, Hội nhập...
    CAP_HD TEXT,                    -- Cấp: Chi hội, Liên chi, Trường
    START_TIME TEXT,                -- Thời gian bắt đầu
    TIME_OUT TEXT,                  -- Thời gian kết thúc
    DIEM_CONG INTEGER DEFAULT 0,     -- Số điểm cộng khi tham gia
    CO_XAC_NHAN TEXT,
    NGAY_TO_CHUC TEXT,  -- Ngày tổ chức
    ID_HK INTEGER,
    FOREIGN KEY (ID_HK) REFERENCES HK_NK(ID_HK)
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
CREATE TABLE IF NOT EXISTS DIEM_DANH_HOAT_DONG (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    MSSV TEXT,
    id_hoat_dong INTEGER,
    thoi_gian TEXT,
    diem_cong INTEGER,
    id_hk INTEGER,
    FOREIGN KEY (id_hoat_dong) REFERENCES HOAT_DONG(ID_HD),
    FOREIGN KEY (id_hk) REFERENCES HK_NK(ID_HK),
    FOREIGN KEY (mssv) REFERENCES SINH_VIEN(MSSV)
);

''')

conn.commit()
conn.close()

# ----------------- CÁC HÀM XỬ LÝ DỮ LIỆU ------------------

def create_table_sinh_vien():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SINH_VIEN (
            ID_SV INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME_SV TEXT NOT NULL,
            MSSV TEXT UNIQUE,
            EMAIL_SV TEXT UNIQUE,
            ADDRESS_SV TEXT,
            DATE_SV DATE,
            SEX_SV INTEGER CHECK (SEX_SV IN (0, 1)),
            CLASS_SV TEXT,
            PASSWORD_SV TEXT NOT NULL,
            TONG_DIEM_HD INTEGER DEFAULT 0,
            FACE_ENCODING TEXT,
            CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

def insert_sinh_vien(name, mssv, email, address, birthdate, gender, class_sv, password, encoding_json, phone):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO SINH_VIEN (
                NAME_SV, MSSV, EMAIL_SV, ADDRESS_SV,
                DATE_SV, SEX_SV, CLASS_SV,
                PASSWORD_SV, FACE_ENCODING, PHONE_SV
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, mssv, email, address, birthdate, gender, class_sv, password, encoding_json, phone))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise Exception(f"Trùng MSSV hoặc Email: {e}")
    finally:
        conn.close()


def get_all_sinh_vien():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT 
            ID_SV, NAME_SV, MSSV, EMAIL_SV, ADDRESS_SV, DATE_SV, SEX_SV,
            CLASS_SV, PASSWORD_SV, TONG_DIEM_HD, FACE_ENCODING, CREATED_AT, PHONE_SV
        FROM SINH_VIEN
    ''')
    rows = c.fetchall()
    conn.close()

    result = []
    for row in rows:
        try:
            encodings = json.loads(row[10]) if row[10] else []  # ✅ Đã sửa index đúng
        except:
            encodings = []

        result.append({
            'id': row[0],
            'name': row[1],
            'mssv': row[2],
            'email': row[3],
            'address': row[4],
            'date': row[5],
            'sex': row[6],
            'class': row[7],
            'password': row[8],
            'TONG_DIEM_HD': row[9],
            'encodings': encodings,
            'created_at': row[11],
            'phone': row[12]
        })

    return result


def sinh_vien_exists(name_sv):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM SINH_VIEN WHERE NAME_SV = ?", (name_sv,))
    result = c.fetchone()
    conn.close()
    return result is not None

def reset_sinh_vien_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS SINH_VIEN")
    conn.commit()
    conn.close()

def reset_and_create_sinh_vien_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS SINH_VIEN")
    c.execute('''
        CREATE TABLE SINH_VIEN (
            ID_SV INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME_SV TEXT NOT NULL,
            MSSV TEXT UNIQUE,
            EMAIL_SV TEXT UNIQUE,
            ADDRESS_SV TEXT,
            DATE_SV DATE,
            SEX_SV INTEGER CHECK (SEX_SV IN (0, 1)),
            CLASS_SV TEXT,
            PASSWORD_SV TEXT NOT NULL,
            TONG_DIEM_HD INTEGER DEFAULT 0,
            FACE_ENCODING TEXT,
            CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP

        );
    ''')
    conn.commit()
    conn.close()

def delete_sinh_vien_by_mssv(mssv):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM SINH_VIEN WHERE MSSV = ?", (mssv,))
    conn.commit()
    conn.close()

def update_sinh_vien(id_sv, name, mssv, email, address, birthdate, gender, class_sv, password, phone):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE SINH_VIEN
        SET NAME_SV = ?, MSSV = ?, EMAIL_SV = ?, ADDRESS_SV = ?, DATE_SV = ?, SEX_SV = ?, CLASS_SV = ?, PASSWORD_SV = ?, PHONE_SV = ?
        WHERE ID_SV = ?
    ''', (name, mssv, email, address, birthdate, gender, class_sv, password, phone, id_sv))
    conn.commit()
    conn.close()





print("✅ Tạo cơ sở dữ liệu và các bảng thành công.")