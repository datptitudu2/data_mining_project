"""
SCRIPT NẠP DỮ LIỆU VÀO STAR SCHEMA & TRUY VẤN OLAP MẪU
Phụ trách: Trần Văn Minh
Input: data_samples/silver_user_behavior_sample.csv (do Đạt cung cấp)
"""

import os
import sys
import duckdb
import pandas as pd

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAMPLE_DATA = os.path.join(BASE_DIR, "data_samples", "silver_user_behavior_sample.csv")
SQL_FILE = os.path.join(os.path.dirname(__file__), "schema_ddl.sql")

con = duckdb.connect()

print("=== 1. TẠO CÁC BẢNG STAR SCHEMA TRONG DUCKDB ===")
with open(SQL_FILE, "r", encoding="utf-8") as f:
    con.execute(f.read())
print("✅ Đã tạo các bảng: Dim_User, Dim_Department, Dim_Time, Fact_DLP_Incident")

print("\n=== 2. NẠP DỮ LIỆU TỪ TẦNG SILVER VÀO DWH ===")
# 2.1 Nạp Dim_User
con.execute(f"""
INSERT INTO Dim_User
SELECT DISTINCT 
    user_id AS user_key,
    user_id,
    role_title,
    dept_name
FROM read_csv_auto('{SAMPLE_DATA}')
ON CONFLICT (user_key) DO NOTHING;
""")

# 2.2 Nạp Dim_Time
con.execute(f"""
INSERT INTO Dim_Time
SELECT DISTINCT 
    strftime(CAST(date AS DATE), '%Y%m%d') AS time_key,
    CAST(date AS DATE) AS event_date,
    EXTRACT(dow FROM CAST(date AS DATE)) AS day_of_week,
    EXTRACT(month FROM CAST(date AS DATE)) AS month,
    CASE WHEN EXTRACT(dow FROM CAST(date AS DATE)) IN (0, 6) THEN 1 ELSE 0 END AS is_weekend
FROM read_csv_auto('{SAMPLE_DATA}')
ON CONFLICT (time_key) DO NOTHING;
""")

# 2.3 Nạp Fact_DLP_Incident
con.execute(f"""
INSERT INTO Fact_DLP_Incident
SELECT 
    user_id || '_' || strftime(CAST(date AS DATE), '%Y%m%d') AS incident_id,
    user_id AS user_key,
    dept_name AS dept_key,
    strftime(CAST(date AS DATE), '%Y%m%d') AS time_key,
    logon_count,
    after_hours_logon,
    usb_connect_count,
    after_hours_usb,
    approx_transfer_bytes AS transfer_bytes,
    CASE WHEN after_hours_usb > 0 OR after_hours_logon > 2 THEN 1 ELSE 0 END AS is_after_hours_incident,
    0.0 AS risk_score
FROM read_csv_auto('{SAMPLE_DATA}')
ON CONFLICT (incident_id) DO NOTHING;
""")

cnt = con.execute("SELECT count(*) FROM Fact_DLP_Incident").fetchone()[0]
print(f"✅ Đã nạp thành công {cnt:,} sự cố vào Fact_DLP_Incident!")

print("\n=== 3. TRUY VẤN OLAP MẪU (ROLL-UP THEO PHÒNG BAN & HÀNH VI NGOÀI GIỜ) ===")
q_olap = """
SELECT 
    f.dept_key AS Phong_Ban,
    count(*) AS Tong_So_Ngay_Giam_Sat,
    sum(f.after_hours_usb) AS Tong_Lan_Cam_USB_Ngoai_Gio,
    sum(f.after_hours_logon) AS Tong_Dang_Nhap_Ngoai_Gio,
    round(sum(f.transfer_bytes) / 1000000.0, 2) AS Tong_MB_Truyen_Tai
FROM Fact_DLP_Incident f
GROUP BY f.dept_key
ORDER BY Tong_Lan_Cam_USB_Ngoai_Gio DESC;
"""
df_olap = con.execute(q_olap).df()
print(df_olap.to_string(index=False))

print("\n[XONG] Script DWH hoạt động hoàn hảo! Minh có thể viết thêm các câu truy vấn Drill-down/Slice-Dice vào đây.")
