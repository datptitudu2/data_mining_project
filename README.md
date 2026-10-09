# 🛡️ HỆ THỐNG KHO DỮ LIỆU & KHAI PHÁ DỮ LIỆU DLP ANALYTICS & UEBA

> **Môn học:** Kho dữ liệu & Khai phá dữ liệu (Data Warehouse & Data Mining)  
> **Tên nhóm:** CyberGuardrails  
> **Thành viên nhóm:**  
> 1. **Nguyễn Tiến Đạt** - B23DCCC034  
> 2. **Trần Văn Minh** - B23DCCC114  
> 3. **Trần Đăng Sang** - B23DCCC144  

---

## 🎯 1. Giới thiệu đề tài
Xây dựng giải pháp toàn diện giám sát, phát hiện nguy cơ thất thoát dữ liệu nhạy cảm (**DLP - Data Loss Prevention**) theo chuẩn **Nghị định 13/2023/NĐ-CP** và **PCI-DSS**, kết hợp phân tích hành vi bất thường của người dùng (**UEBA - User and Entity Behavior Analytics**) để phát hiện hiểm họa nội gián (*Insider Threat*).

### 4 Phân hệ Khai phá tri thức (Data Mining Modules):
1. **Phân lớp văn bản nhạy cảm (Text Classification)**: Tự động phân loại tài liệu vào 4 cấp độ: *Public*, *Internal*, *Confidential*, *Secret*.
2. **Phát hiện hành vi bất thường (UEBA Anomaly Detection)**: Sử dụng mô hình **Isolation Forest** chấm điểm nguy cơ rủi ro.
3. **Khai phá luật kết hợp rò rỉ (Association Rules Mining)**: Áp dụng thuật toán **FP-Growth** tìm mẫu hành vi vi phạm thường đi liền với nhau.
4. **Phân cụm hồ sơ rủi ro (Clustering)**: Thuật toán **K-Means** gom nhóm người dùng theo mức độ an toàn.

---

## 🏗️ 2. Kiến trúc Hồ dữ liệu (Lakehouse Medallion Architecture)

```
[Raw Sources: Logs USB/Web/Logon + Enron Email + Synthetic PII]
                           │
                           ▼ (Ingestion Pipeline)
           ┌───────────────────────────────┐
           │   BRONZE LAYER (Data Lake)    │  (MinIO S3 / Parquet)
           └───────────────────────────────┘
                           │
                           ▼ (ELT, Profiling, PII Masking)
           ┌───────────────────────────────┐
           │   SILVER LAYER (Staging)      │  (Làm sạch, gắn nhãn rủi ro)
           └───────────────────────────────┘
                           │
                           ▼ (Star Schema Modeling)
           ┌───────────────────────────────┐
           │   GOLD LAYER (DWH Star)       │  (DuckDB / PostgreSQL)
           │ Fact_DLP_Incident + Dim_Tables│
           └───────────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
  [Data Mining Engines]          [BI Dashboard / OLAP]
(Isolation Forest, NLP, K-Means)      (Streamlit)
```

---

## 🚀 3. Hướng dẫn cài đặt & Khởi chạy cho thành viên nhóm

### Bước 1: Khởi động Hạ tầng Docker (MinIO S3 & PostgreSQL DWH)
```bash
docker-compose up -d
```
* **MinIO Console**: http://localhost:9001 (User: `minioadmin` / Pass: `minioadmin123`)
* **MinIO S3 Endpoint**: http://localhost:9000
* **PostgreSQL DWH**: `localhost:5432` (User: `dataeng` / Pass: `dataeng123` / DB: `dwh`)

### Bước 2: Thiết lập môi trường Python ảo
```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Cài đặt thư viện cần thiết
pip install pandas duckdb s3fs pyarrow psycopg2-binary scikit-learn matplotlib seaborn jupyter
```

### Bước 3: Đồng bộ Dataset
* Xem hướng dẫn cấu trúc dữ liệu tại [datasets/README.md](datasets/README.md).
* Tải bộ log đầy đủ từ Google Drive của nhóm và giải nén vào thư mục `datasets/`.

---

## 📂 4. Phân công công việc (Task Assignment)

| Thành viên | Nhiệm vụ chính | Trạng thái |
| :--- | :--- | :--- |
| **Nguyễn Tiến Đạt** | Kiến trúc Data Lake Bronze/Silver, pipeline Ingestion & Masking PII | Đã hoàn thành Bài 1, Bài 2 |
| **Trần Văn Minh** | Thiết kế Star Schema (Gold Layer), xây dựng Fact_DLP_Incident & DuckDB OLAP | Đang triển khai |
| **Trần Đăng Sang** | Phát triển mô hình Data Mining (Isolation Forest UEBA & Phân loại văn bản) | Đang triển khai |
