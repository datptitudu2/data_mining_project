import os
import duckdb
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DIR = os.path.join(BASE_DIR, "data_samples")
os.makedirs(SAMPLE_DIR, exist_ok=True)

con = duckdb.connect()

print("=== Dang tong hop du lieu Silver Mau cho Minh & Sang ===")

# 1. Doc log USB
usb_path = os.path.join(BASE_DIR, "datasets", "cmu_cert", "r1", "device.csv")
# 2. Doc log Logon
logon_path = os.path.join(BASE_DIR, "datasets", "cmu_cert", "r1", "logon.csv")
# 3. Doc LDAP HR
ldap_path = os.path.join(BASE_DIR, "datasets", "cmu_cert", "r1", "LDAP", "2010-05.csv")

# Query duckdb tong hop hanh vi theo ngay cho 1,000 nhan vien mau
query = f"""
WITH usb_clean AS (
    SELECT 
        user AS user_id,
        CAST(strptime(date, '%m/%d/%Y %H:%M:%S') AS DATE) AS event_date,
        COUNT(*) AS usb_connect_count,
        SUM(CASE 
            WHEN EXTRACT(hour FROM strptime(date, '%m/%d/%Y %H:%M:%S')) < 8 
              OR EXTRACT(hour FROM strptime(date, '%m/%d/%Y %H:%M:%S')) >= 18 
              OR EXTRACT(dow FROM strptime(date, '%m/%d/%Y %H:%M:%S')) IN (0, 6) 
            THEN 1 ELSE 0 
        END) AS after_hours_usb
    FROM read_csv_auto('{usb_path}')
    WHERE user IS NOT NULL
    GROUP BY user, CAST(strptime(date, '%m/%d/%Y %H:%M:%S') AS DATE)
),
logon_clean AS (
    SELECT 
        user AS user_id,
        CAST(strptime(date, '%m/%d/%Y %H:%M:%S') AS DATE) AS event_date,
        COUNT(*) AS logon_count,
        SUM(CASE 
            WHEN EXTRACT(hour FROM strptime(date, '%m/%d/%Y %H:%M:%S')) < 8 
              OR EXTRACT(hour FROM strptime(date, '%m/%d/%Y %H:%M:%S')) >= 18 
              OR EXTRACT(dow FROM strptime(date, '%m/%d/%Y %H:%M:%S')) IN (0, 6) 
            THEN 1 ELSE 0 
        END) AS after_hours_logon
    FROM read_csv_auto('{logon_path}')
    WHERE user IS NOT NULL
    GROUP BY user, CAST(strptime(date, '%m/%d/%Y %H:%M:%S') AS DATE)
),
hr_info AS (
    SELECT 
        user_id,
        Domain AS dept_name,
        Role AS role_title
    FROM read_csv_auto('{ldap_path}')
)
SELECT 
    l.user_id,
    l.event_date AS date,
    COALESCE(h.dept_name, 'IT & Engineering') AS dept_name,
    COALESCE(h.role_title, 'Staff') AS role_title,
    l.logon_count,
    l.after_hours_logon,
    COALESCE(u.usb_connect_count, 0) AS usb_connect_count,
    COALESCE(u.after_hours_usb, 0) AS after_hours_usb,
    COALESCE(u.usb_connect_count, 0) * 15000000 AS approx_transfer_bytes
FROM logon_clean l
LEFT JOIN usb_clean u ON l.user_id = u.user_id AND l.event_date = u.event_date
LEFT JOIN hr_info h ON l.user_id = h.user_id
WHERE l.event_date BETWEEN '2010-05-01' AND '2010-05-31'
LIMIT 5000;
"""

df_sample = con.execute(query).df()
print(f"Tong hop thanh cong {len(df_sample):,} ban ghi mau!")

out_csv = os.path.join(SAMPLE_DIR, "silver_user_behavior_sample.csv")
df_sample.to_csv(out_csv, index=False)
print(f"[DA LUU] File du lieu mau tai: {out_csv}")
