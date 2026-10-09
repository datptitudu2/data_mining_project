"""
HUONG DAN THUC HANH DECISION TREE VOI EMAIL SPAM CLASSIFICATION DATASET
=======================================================================
Bai toan: Phan loai email la Spam (1) hay Ham/Hop thu binh thuong (0).
Dac diem du lieu:
  - Du lieu dang Bag-of-Words (tan suat tu vung)
  - 5,172 mau email
  - 3,002 cot (1 cot dinh danh 'Email No.', 3,000 cot tan suat tu, 1 cot muc tieu 'Prediction')
  - So luong chieu (features) rat lon (High Dimensionality), doi hoi phai cat tia (Pruning)
    de tranh cay qua sau gay Overfitting.

Cac buoc thuc hien:
Buoc 1: Load du lieu & Kiem tra kich thuoc
Buoc 2: Tien xu ly (Loai bo cot dinh danh khong co y nghia hoc may)
Buoc 3: Phan tich phan bo lop (Class Balance)
Buoc 4: Chia tap du lieu Train/Test (80/20)
Buoc 5: Xay dung mo hinh Decision Tree & Kiem soat do sau (max_depth)
Buoc 6: Danh gia mo hinh toan dien (Accuracy, Precision, Recall, F1, Confusion Matrix)
Buoc 7: Kham pha cac tu khoa dac trung nhat (Top Spam/Ham keywords dua tren Feature Importance)
Buoc 8: Truc quan hoa cay quyet dinh (Decision Tree Visualization)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)

# Thiet lap duong dan
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "email_spam", "emails.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_email_spam")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 
# BUOC 1: LOAD DU LIEU VA KIEM TRA
# 
print("=" * 60)
print("BUOC 1: LOAD DU LIEU EMAIL SPAM CLASSIFICATION")
print("=" * 60)

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Khong tim thay file {DATA_PATH}. Vui long chay download_data.py truoc!")

df = pd.read_csv(DATA_PATH)
print(f"Kich thuoc du lieu: {df.shape[0]} dong, {df.shape[1]} cot")
print("\nCac cot dau va cuoi:")
print(list(df.columns[:5]) + ["..."] + list(df.columns[-3:]))

# 
# BUOC 2: TIEN XU LY DU LIEU (DATA PREPROCESSING)
# 
print("\n" + "=" * 60)
print("BUOC 2: TIEN XU LY DU LIEU")
print("=" * 60)

# Cot 'Email No.' chi la dinh danh (ID), khong mang y nghia quy luat => Can loai bo
if 'Email No.' in df.columns:
    df = df.drop(columns=['Email No.'])
    print("[+] Da loai bo cot 'Email No.'")

# Tach X (features) va y (label)
X = df.drop(columns=['Prediction'])
y = df['Prediction']

# Kiem tra missing value
null_count = X.isnull().sum().sum()
print(f"Tong so gia tri null: {null_count}")

# 
# BUOC 3: PHAN TICH PHAN BO NHO (CLASS DISTRIBUTION)
# 
print("\n" + "=" * 60)
print("BUOC 3: PHAN BO CAC LOP (HAM vs SPAM)")
print("=" * 60)

counts = y.value_counts()
print(f"Ham (0 - Email binh thuong): {counts.get(0, 0)} ({counts.get(0, 0)/len(y)*100:.1f}%)")
print(f"Spam (1 - Thu rac):         {counts.get(1, 0)} ({counts.get(1, 0)/len(y)*100:.1f}%)")

# 
# BUOC 4: CHIA TAP TRAIN / TEST (80/20)
# 
print("\n" + "=" * 60)
print("BUOC 4: CHIA TAP TRAIN / TEST (80/20)")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"So mau Train: {X_train.shape[0]} mau x {X_train.shape[1]} dac trung")
print(f"So mau Test:  {X_test.shape[0]} mau x {X_test.shape[1]} dac trung")

# 
# BUOC 5: HUAN LUYEN VA TOI UU HOA DECISION TREE
# 
print("\n" + "=" * 60)
print("BUOC 5: HUAN LUYEN DECISION TREE & DANH GIA CAC DO SAU (MAX_DEPTH)")
print("=" * 60)

# 1. Thu nghiem cac do sau de xem muc do anh huong toi Overfitting
depths = [3, 5, 8, 12, 15, None]
depth_results = []

for d in depths:
    clf = DecisionTreeClassifier(max_depth=d, random_state=42)
    clf.fit(X_train, y_train)
    tr_acc = accuracy_score(y_train, clf.predict(X_train))
    te_acc = accuracy_score(y_test, clf.predict(X_test))
    d_label = f"depth={d}" if d else "depth=Unconstrained"
    depth_results.append((d_label, tr_acc, te_acc, clf.get_depth()))
    print(f"[*] {d_label:20s} -> Train Acc: {tr_acc:.4f} | Test Acc: {te_acc:.4f} | Actual Depth: {clf.get_depth()}")

# Chon mo hinh tot nhat (can bang giua toc do, de giai thich va do chinh xac cao)
# Thuong max_depth tu 8-10 mang lai hieu qua cao tren tap email ma khong qua nong
best_tree = DecisionTreeClassifier(
    criterion='gini',
    max_depth=8,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
best_tree.fit(X_train, y_train)

# 
# BUOC 6: DANH GIA CHI TIET MO HINH
# 
print("\n" + "=" * 60)
print("BUOC 6: DANH GIA CHI TIET MO HINH (TEST SET)")
print("=" * 60)

y_pred = best_tree.predict(X_test)

print("\n--- CLASSIFICATION REPORT ---")
print(classification_report(y_test, y_pred, target_names=['Ham (0)', 'Spam (1)']))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Du doan Ham (0)', 'Du doan Spam (1)'],
            yticklabels=['Thuc te Ham (0)', 'Thuc te Spam (1)'])
plt.title("Email Spam - Decision Tree Confusion Matrix")
plt.ylabel("Nhan Thuc Te")
plt.xlabel("Nhan Du Doan")
plt.tight_layout()
cm_path = os.path.join(OUTPUT_DIR, "email_spam_confusion_matrix.png")
plt.savefig(cm_path, dpi=300)
plt.close()
print(f"[DA LUU] Bieu do Confusion Matrix tai: {cm_path}")

# 
# BUOC 7: TOP CAC TU KHOA QUAN TRONG NHAT (FEATURE IMPORTANCE)
# 
print("\n" + "=" * 60)
print("BUOC 7: TOP CAC TU KHOA QUYET DINH PHAN LOAI SPAM")
print("=" * 60)

importances = best_tree.feature_importances_
feat_imp = pd.Series(importances, index=X.columns).sort_values(ascending=False)

print("Top 15 tu vung duoc cay quyet dinh dung nhieu nhat:")
for word, imp in feat_imp.head(15).items():
    print(f"  - '{word:15s}': {imp:.4f}")

plt.figure(figsize=(10, 6))
feat_imp.head(15).plot(kind='barh', color='#2e7d32')
plt.gca().invert_yaxis()
plt.title("Email Spam - Top 15 Most Important Words (Decision Tree)")
plt.xlabel("Gini Feature Importance")
plt.tight_layout()
fi_path = os.path.join(OUTPUT_DIR, "email_spam_feature_importance.png")
plt.savefig(fi_path, dpi=300)
plt.close()
print(f"[DA LUU] Bieu do Feature Importance tai: {fi_path}")

# 
# BUOC 8: TRUC QUAN HOA NHANH CAY QUYET DINH (SUB-TREE VISUALIZATION)
# 
print("\n" + "=" * 60)
print("BUOC 8: TRUC QUAN HOA CAY QUYET DINH (3 TANG DAU)")
print("=" * 60)

# Ve 3 tang dau tien cua cay de quan sat luat re nhanh (IF-THEN rules)
plt.figure(figsize=(26, 12))
plot_tree(
    best_tree,
    max_depth=3, # Gioi han hien thi 3 tang dau de ro net, khong bi roi
    feature_names=list(X.columns),
    class_names=['Ham', 'Spam'],
    filled=True,
    rounded=True,
    fontsize=11
)
plt.title("Email Spam Decision Tree (Top 3 Levels of Decision Rules)", fontsize=16)
tree_path = os.path.join(OUTPUT_DIR, "email_spam_decision_tree_top3.png")
plt.savefig(tree_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"[DA LUU] Anh so do luat cay quyet dinh tai: {tree_path}")

print("\nHOAN TAT XU LY EMAIL SPAM DATASET!")
