import sqlite3

# Tạo file CSDL SQLite
conn = sqlite3.connect("ql_hoatdong.db")
cursor = conn.cursor()

# Bảng Khoa
cursor.execute("""
CREATE TABLE Khoa (
    Id_khoa INTEGER PRIMARY KEY,
    Name_khoa TEXT
);
""")

# Bảng Học kỳ - Năm học
cursor.execute("""
CREATE TABLE HK_NK (
    Id_hk INTEGER PRIMARY KEY,
    School_year TEXT
);
""")

# Bảng Sinh viên
cursor.execute("""
CREATE TABLE Sinh_vien (
    Id_sv INTEGER PRIMARY KEY,
    Name_sv TEXT,
    Address_sv TEXT,
    Date_sv DATE,
    Sex_sv BOOLEAN,
    Class_sv TEXT
);
""")

# Bảng Hoạt động
cursor.execute("""
CREATE TABLE Hoat_dong (
    Id_hd INTEGER PRIMARY KEY,
    Time_out DATETIME,
    Start_time DATETIME,
    Category_hd TEXT
);
""")

# Bảng Tham gia (Nhiều-nhiều: Sinh_vien - Hoat_dong)
cursor.execute("""
CREATE TABLE Tham_gia (
    Id_sv INTEGER,
    Id_hd INTEGER,
    PRIMARY KEY (Id_sv, Id_hd),
    FOREIGN KEY (Id_sv) REFERENCES Sinh_vien(Id_sv),
    FOREIGN KEY (Id_hd) REFERENCES Hoat_dong(Id_hd)
);
""")

# Bảng Tạo (Nhiều-nhiều: Khoa - Hoat_dong)
cursor.execute("""
CREATE TABLE Tao (
    Id_khoa INTEGER,
    Id_hd INTEGER,
    PRIMARY KEY (Id_khoa, Id_hd),
    FOREIGN KEY (Id_khoa) REFERENCES Khoa(Id_khoa),
    FOREIGN KEY (Id_hd) REFERENCES Hoat_dong(Id_hd)
);
""")

# Bảng Điểm danh (Nhiều-nhiều-nhiều: Sinh_vien - Hoat_dong - HK_NK)
cursor.execute("""
CREATE TABLE Diem_danh (
    Id_sv INTEGER,
    Id_hd INTEGER,
    Id_hk INTEGER,
    PRIMARY KEY (Id_sv, Id_hd, Id_hk),
    FOREIGN KEY (Id_sv) REFERENCES Sinh_vien(Id_sv),
    FOREIGN KEY (Id_hd) REFERENCES Hoat_dong(Id_hd),
    FOREIGN KEY (Id_hk) REFERENCES HK_NK(Id_hk)
);
""")

conn.commit()
conn.close()
print("Cơ sở dữ liệu đã tạo thành công!")
