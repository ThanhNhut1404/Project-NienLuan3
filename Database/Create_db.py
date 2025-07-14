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
    PASSWORD_SV TEXT NOT NULL,
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
            FACE_ENCODING TEXT,
            CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

def insert_sinh_vien(name, mssv, email, address, birthdate, gender, class_sv, password, encoding_json):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO SINH_VIEN (
                NAME_SV, MSSV, EMAIL_SV, ADDRESS_SV,
                DATE_SV, SEX_SV, CLASS_SV,
                PASSWORD_SV, FACE_ENCODING
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, mssv, email, address, birthdate, gender, class_sv, password, encoding_json))
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
            CLASS_SV, PASSWORD_SV, FACE_ENCODING, CREATED_AT
        FROM SINH_VIEN
    ''')
    rows = c.fetchall()
    conn.close()

    result = []
    for row in rows:
        try:
            encodings = json.loads(row[9]) if row[9] else []
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
            'encodings': encodings,
            'created_at': row[10]
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

def update_sinh_vien(mssv, name, email, address, birthdate, gender, class_sv):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE SINH_VIEN
        SET NAME_SV = ?, EMAIL_SV = ?, ADDRESS_SV = ?, DATE_SV = ?, SEX_SV = ?, CLASS_SV = ?
        WHERE MSSV = ?
    ''', (name, email, address, birthdate, gender, class_sv, mssv))
    conn.commit()
    conn.close()



print("✅ Tạo cơ sở dữ liệu và các bảng thành công.")