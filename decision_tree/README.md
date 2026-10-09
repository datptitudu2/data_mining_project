# 🌳 THỰC HÀNH THUẬT TOÁN DECISION TREE (CÂY QUYẾT ĐỊNH) TRONG DATA MINING & MACHINE LEARNING

Thư mục này chứa toàn bộ dữ liệu, mã nguồn (Scripts & Jupyter Notebook), mô hình huấn luyện và kết quả trực quan hóa cho 2 bộ dữ liệu kinh điển từ Kaggle:

1. **Titanic: Machine Learning from Disaster** (Phân loại dữ liệu bảng - Tabular Classification).
2. **Email Spam Classification Dataset** (Phân loại dữ liệu văn bản tần suất từ - Bag-of-Words Classification).

---

## 📁 Cấu trúc thư mục

```
f:\data-mining\decision_tree\
│
├── titanic\                               # Thư mục chứa dữ liệu Titanic
│   ├── train.csv                          # Dữ liệu huấn luyện (891 mẫu)
│   ├── test.csv                           # Dữ liệu kiểm thử Kaggle (418 mẫu)
│   └── gender_submission.csv              # Mẫu nộp bài Kaggle
│
├── email_spam\                            # Thư mục chứa dữ liệu Email Spam
│   └── emails.csv                         # 5,172 email x 3,002 cột đặc trưng
│
├── output_titanic\                        # Kết quả & Biểu đồ của Titanic
│   ├── titanic_decision_tree.png          # Sơ đồ trực quan hóa Cây quyết định
│   ├── titanic_confusion_matrix.png       # Ma trận nhầm lẫn
│   ├── titanic_feature_importance.png     # Đồ thị mức độ quan trọng đặc trưng
│   └── titanic_submission.csv             # File dự đoán nộp bài Kaggle
│
├── output_email_spam\                     # Kết quả & Biểu đồ của Email Spam
│   ├── email_spam_decision_tree_top3.png  # Sơ đồ 3 tầng đầu luật phân loại
│   ├── email_spam_confusion_matrix.png    # Ma trận nhầm lẫn
│   └── email_spam_feature_importance.png  # Top 15 từ khóa phát hiện Spam
│
├── Huong_Dan_Decision_Tree.ipynb          # Jupyter Notebook thực hành từng bước trực quan
├── 01_decision_tree_titanic.py            # Mã nguồn Python xử lý Titanic
├── 02_decision_tree_email_spam.py         # Mã nguồn Python xử lý Email Spam
└── download_data.py                       # Script tự động tải bộ dữ liệu
```

---

## 🚀 Cách chạy chương trình

### Cách 1: Chạy bằng Jupyter Notebook (Trực quan, từng bước)
Mở file `Huong_Dan_Decision_Tree.ipynb` trong VS Code / Antigravity IDE hoặc Jupyter Lab, chọn Python Kernel `.venv`, rồi bấm **Run All**.

### Cách 2: Chạy trực tiếp bằng lệnh Python terminal
```bash
# Kích hoạt môi trường ảo
& "f:\data-mining\.venv\Scripts\Activate.ps1"

# Chạy mô hình Titanic
python f:\data-mining\decision_tree\01_decision_tree_titanic.py

# Chạy mô hình Email Spam
python f:\data-mining\decision_tree\02_decision_tree_email_spam.py
```
