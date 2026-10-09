# 📦 HƯỚNG DẪN CẤU TRÚC & ĐỒNG BỘ DATASET ĐỀ TÀI DLP ANALYTICS

Hệ thống sử dụng 3 nguồn dữ liệu theo đúng bản thuyết minh đề tài:

```
datasets/
├── cmu_cert/                 # Log hành vi người dùng (CMU CERT Insider Threat)
│   ├── r1/                   # Log thô (device.csv, http.csv, logon.csv, LDAP/)
│   └── answers/              # Ground truth kịch bản nội gián để đánh giá mô hình
│
├── enron/                    # Dữ liệu văn bản Email (Enron Email Corpus - 1.42 GB)
│   └── emails.csv            # Dùng cho phân hệ phân loại rò rỉ qua Email
│
└── synthetic_pii/            # Dữ liệu văn bản nhạy cảm mô phỏng theo Nghị định 13 & PCI-DSS
    ├── public/               # Cấp độ Public (Thông cáo báo chí, HDSD)
    ├── internal/             # Cấp độ Internal (Kế hoạch tuần, phân công trực)
    ├── confidential/         # Cấp độ Confidential (Bảng lương, danh sách khách hàng VIP)
    └── secret/               # Cấp độ Secret (API keys, số thẻ tín dụng PCI-DSS)
```

> **Lưu ý quan trọng cho các thành viên nhóm:**
> Do các file `emails.csv` (1.42 GB) và `http.csv` (304 MB) vượt quá giới hạn 100 MB của GitHub, các file này đã được đưa vào `.gitignore`. 
> Thành viên mới clone repo về vui lòng tải bộ dữ liệu đầy đủ từ link Google Drive nội bộ của nhóm và đặt đúng vào đường dẫn `datasets/` như trên.
