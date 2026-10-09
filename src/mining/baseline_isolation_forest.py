"""
MÔ HÌNH BASELINE PHÁT HIỆN HÀNH VI BẤT THƯỜNG (UEBA - ISOLATION FOREST)
Phụ trách: Trần Đăng Sang (Data Mining Specialist)
Input: data_samples/silver_user_behavior_sample.csv (do Đạt cung cấp)
Output: Bảng xếp hạng nhân viên rủi ro + Biểu đồ phân bố Anomaly Score
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAMPLE_DATA = os.path.join(BASE_DIR, "data_samples", "silver_user_behavior_sample.csv")
OUTPUT_DIR = os.path.dirname(__file__)

print("=== 1. NẠP DỮ LIỆU ĐẶC TRƯNG HÀNH VI (TẦNG SILVER) ===")
df = pd.read_csv(SAMPLE_DATA)
print(f"Tổng số bản ghi giám sát: {len(df):,}")

# Chọn các đặc trưng hành vi số học
feature_cols = [
    'logon_count',
    'after_hours_logon',
    'usb_connect_count',
    'after_hours_usb',
    'approx_transfer_bytes'
]
X = df[feature_cols].fillna(0)
print("Các đặc trưng hành vi đưa vào mô hình:")
print(feature_cols)

print("\n=== 2. HUẤN LUYỆN MÔ HÌNH ISOLATION FOREST ===")
# contamination=0.01: Giả định khoảng 1% hành vi là bất thường/nguy hiểm
iso_model = IsolationForest(
    n_estimators=100,
    contamination=0.01,
    random_state=42,
    n_jobs=-1
)
iso_model.fit(X)

# Dự đoán: -1 là bất thường, 1 là bình thường
df['is_anomaly'] = iso_model.predict(X)
# Decision function: Điểm càng âm thì càng dị biệt (càng bất thường)
df['anomaly_score'] = -iso_model.decision_function(X)

anomalies = df[df['is_anomaly'] == -1]
print(f"✅ Phát hiện {len(anomalies)} sự kiện bất thường ({len(anomalies)/len(df)*100:.1f}%)")

print("\n=== 3. TOP 10 NHÂN VIÊN CÓ NGUY CƠ NỘI GIÁN CAO NHẤT ===")
top_risks = df.sort_values(by='anomaly_score', ascending=False)[
    ['user_id', 'date', 'role_title', 'after_hours_usb', 'after_hours_logon', 'anomaly_score']
].head(10)
print(top_risks.to_string(index=False))

print("\n=== 4. VẼ BIỂU ĐỒ PHÂN BỐ ANOMALY SCORE ===")
plt.figure(figsize=(9, 5))
plt.hist(df['anomaly_score'], bins=40, color='#3b82f6', edgecolor='black', alpha=0.7)
plt.axvline(
    x=df[df['is_anomaly'] == -1]['anomaly_score'].min(), 
    color='red', linestyle='--', linewidth=2, label='Ngưỡng báo động (Anomaly Threshold)'
)
plt.title("UEBA - Phân bố điểm số bất thường (Isolation Forest)", fontsize=13)
plt.xlabel("Anomaly Score (Điểm càng cao càng rủi ro)")
plt.ylabel("Số lượng bản ghi")
plt.legend()
plt.tight_layout()

chart_path = os.path.join(OUTPUT_DIR, "anomaly_score_distribution.png")
plt.savefig(chart_path, dpi=300)
plt.close()
print(f"✅ Đã lưu biểu đồ tại: {chart_path}")
print("\n[XONG] Mô hình Baseline hoàn tất! Sang có thể thử nghiệm thêm các tham số hoặc bổ sung đặc trưng.")
