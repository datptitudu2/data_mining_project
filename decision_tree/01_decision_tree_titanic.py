"""
HUONG DAN THUC HANH DECISION TREE VOI DATASET TITANIC
=====================================================
Bai toan: Du doan kha nang song sot (Survived: 0 = Khong, 1 = Co) cua hanh khach.
Dac diem du lieu: Du lieu bang hon hop (so hoc + phan loai), co du lieu khuyet (missing values).

Cac buoc thuc hien:
Buoc 1: Load du lieu & Kham pha (EDA)
Buoc 2: Tien xu ly du lieu (Xu ly Missing values & Encoding)
Buoc 3: Ky thuat tao dac trung (Feature Engineering)
Buoc 4: Chia tap du lieu Train/Validation (80/20)
Buoc 5: Xay dung mo hinh Decision Tree (So sanh Overfitting vs Regularization)
Buoc 6: Danh gia mo hinh (Accuracy, Precision, Recall, F1, Confusion Matrix)
Buoc 7: Danh gia Feature Importance (Dac trung nao quan trong nhat)
Buoc 8: Truc quan hoa cay quyet dinh (Decision Tree Visualization)
Buoc 9: Du doan tren tap test.csv va xuat file nop Kaggle
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)

# Thiet lap duong dan
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "titanic")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_titanic")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 
# BUOC 1: LOAD DU LIEU VA KHAM PHA (EDA)
# 
print("=" * 60)
print("BUOC 1: LOAD DU LIEU VA KHAM PHA (EDA)")
print("=" * 60)

train_path = os.path.join(DATA_DIR, "train.csv")
test_path = os.path.join(DATA_DIR, "test.csv")

df_train = pd.read_csv(train_path)
df_test = pd.read_csv(test_path)

print(f"Kich thuoc tap train: {df_train.shape[0]} dong, {df_train.shape[1]} cot")
print(f"Kich thuoc tap test:  {df_test.shape[0]} dong, {df_test.shape[1]} cot")
print("\n5 dong dau tien tap train:")
print(df_train.head(3))

print("\nKiem tra gia tri thieu (Missing values) tren tap train:")
missing = df_train.isnull().sum()
print(missing[missing > 0])

# 
# BUOC 2 & 3: TIEN XU LY VA TAO DAC TRUNG (FEATURE ENGINEERING)
# 
print("\n" + "=" * 60)
print("BUOC 2 & 3: TIEN XU LY DU LIEU VA TAO DAC TRUNG")
print("=" * 60)

def preprocess_titanic(df, is_train=True):
    data = df.copy()
    
    # 1. Trích xuất Title từ tên (Mr, Mrs, Miss, Master, v.v.)
    data['Title'] = data['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
    # Gom cac danh xung it gap thanh 'Other'
    common_titles = ['Mr', 'Miss', 'Mrs', 'Master']
    data['Title'] = data['Title'].apply(lambda x: x if x in common_titles else 'Other')
    
    # 2. Xu ly gia tri thieu cho Age (dien theo median theo Title)
    age_median = data.groupby('Title')['Age'].transform('median')
    data['Age'] = data['Age'].fillna(age_median)
    data['Age'] = data['Age'].fillna(data['Age'].median())
    
    # 3. Xu ly Embarked (dien gia tri pho bien nhat 'S')
    data['Embarked'] = data['Embarked'].fillna('S')
    
    # 4. Xu ly Fare (dien gia tri median)
    data['Fare'] = data['Fare'].fillna(data['Fare'].median())
    
    # 5. Tao dac trung moi
    # FamilySize: Tong so thanh vien gia dinh di cung
    data['FamilySize'] = data['SibSp'] + data['Parch'] + 1
    # IsAlone: Hanh khach di mot minh
    data['IsAlone'] = (data['FamilySize'] == 1).astype(int)
    
    # 6. Chuyen doi dac trung danh muc sang so (One-Hot Encoding)
    # Cac cot danh muc can encode: Sex, Embarked, Title, Pclass
    features = ['Pclass', 'Sex', 'Age', 'Fare', 'FamilySize', 'IsAlone', 'Embarked', 'Title']
    processed_df = pd.get_dummies(data[features], columns=['Sex', 'Embarked', 'Title', 'Pclass'], drop_first=True)
    
    return processed_df, (data['Survived'] if is_train else None)

X, y = preprocess_titanic(df_train, is_train=True)
X_kaggle_test, _ = preprocess_titanic(df_test, is_train=False)

# Dong bo cac cot giua train va test (tranh truong hop cot bi lech do One-Hot)
X, X_kaggle_test = X.align(X_kaggle_test, join='left', axis=1, fill_value=0)

print(f"Cac dac trung sau khi tien xu ly ({X.shape[1]} dac trung):")
print(list(X.columns))

# 
# BUOC 4: CHIA TAP TRAIN / VALIDATION (80/20)
# 
print("\n" + "=" * 60)
print("BUOC 4: CHIA TAP TRAIN / VALIDATION (80/20)")
print("=" * 60)

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"So luong mau tap Train: {X_train.shape[0]}")
print(f"So luong mau tap Val:   {X_val.shape[0]}")

# 
# BUOC 5: HUAN LUYEN DECISION TREE (SO SANH OVERFITTING VS REGULARIZATION)
# 
print("\n" + "=" * 60)
print("BUOC 5: HUAN LUYEN DECISION TREE (OVERFITTING VS REGULARIZATION)")
print("=" * 60)

# 1. Decision Tree khong gioi han do sau (De bi Overfitting)
dt_unpruned = DecisionTreeClassifier(random_state=42)
dt_unpruned.fit(X_train, y_train)

train_acc_unpruned = accuracy_score(y_train, dt_unpruned.predict(X_train))
val_acc_unpruned = accuracy_score(y_val, dt_unpruned.predict(X_val))

print(f"[*] Cay khong cat tia (Do sau = {dt_unpruned.get_depth()}):")
print(f"    - Accuracy tren tap Train: {train_acc_unpruned:.4f} (Gan nhu 100% hoc vet)")
print(f"    - Accuracy tren tap Val:   {val_acc_unpruned:.4f}")

# 2. Decision Tree duoc cat tia / gioi han tham so (Tuning de tranh Overfitting)
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [3, 4, 5, 6, 7],
    'min_samples_split': [5, 10, 20],
    'min_samples_leaf': [2, 4, 8]
}

grid_search = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

best_dt = grid_search.best_estimator_
print(f"\n[*] Tham so toi uu tim duoc bang GridSearch (5-Fold CV):")
print(f"    {grid_search.best_params_}")

train_acc_pruned = accuracy_score(y_train, best_dt.predict(X_train))
val_acc_pruned = accuracy_score(y_val, best_dt.predict(X_val))
print(f"[*] Ket qua cua Cay sau khi toi uu:")
print(f"    - Accuracy tren tap Train: {train_acc_pruned:.4f}")
print(f"    - Accuracy tren tap Val:   {val_acc_pruned:.4f}")

# 
# BUOC 6: DANH GIA CHI TIET MO HINH (CLASSIFICATION REPORT & CONFUSION MATRIX)
# 
print("\n" + "=" * 60)
print("BUOC 6: DANH GIA CHI TIET MO HINH")
print("=" * 60)

y_pred = best_dt.predict(X_val)

print("\n--- CLASSIFICATION REPORT ---")
print(classification_report(y_val, y_pred, target_names=['Khong song sot (0)', 'Song sot (1)']))

# Ve Confusion Matrix
cm = confusion_matrix(y_val, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Du doan 0', 'Du doan 1'],
            yticklabels=['Thuc te 0', 'Thuc te 1'])
plt.title("Titanic Decision Tree - Confusion Matrix")
plt.ylabel("Nhan Thuc Te")
plt.xlabel("Nhan Du Doan")
plt.tight_layout()
cm_path = os.path.join(OUTPUT_DIR, "titanic_confusion_matrix.png")
plt.savefig(cm_path, dpi=300)
plt.close()
print(f"[DA LUU] Bieu do Confusion Matrix tai: {cm_path}")

# 
# BUOC 7: PHAN TICH FEATURE IMPORTANCE (DO QUAN TRONG CUA CAC DAC TRUNG)
# 
print("\n" + "=" * 60)
print("BUOC 7: PHAN TICH FEATURE IMPORTANCE")
print("=" * 60)

importances = best_dt.feature_importances_
feat_imp = pd.Series(importances, index=X.columns).sort_values(ascending=False)

print("Top dac trung quan trong nhat:")
for feat, imp in feat_imp.head(7).items():
    print(f"  - {feat:25s}: {imp:.4f}")

plt.figure(figsize=(10, 6))
feat_imp.head(10).plot(kind='barh', color='#2b5c8f')
plt.gca().invert_yaxis()
plt.title("Titanic Decision Tree - Top 10 Feature Importances (Gini Importance)")
plt.xlabel("Do quan trong (Importance Score)")
plt.tight_layout()
fi_path = os.path.join(OUTPUT_DIR, "titanic_feature_importance.png")
plt.savefig(fi_path, dpi=300)
plt.close()
print(f"[DA LUU] Bieu do Feature Importance tai: {fi_path}")

# 
# BUOC 8: TRUC QUAN HOA CAY QUYET DINH (DECISION TREE VISUALIZATION)
# 
print("\n" + "=" * 60)
print("BUOC 8: TRUC QUAN HOA CAY QUYET DINH")
print("=" * 60)

plt.figure(figsize=(24, 12))
plot_tree(
    best_dt,
    feature_names=list(X.columns),
    class_names=['Died', 'Survived'],
    filled=True,
    rounded=True,
    fontsize=10
)
plt.title(f"Titanic Decision Tree (max_depth={best_dt.max_depth})", fontsize=16)
tree_path = os.path.join(OUTPUT_DIR, "titanic_decision_tree.png")
plt.savefig(tree_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"[DA LUU] Anh so do cay quyet dinh tai: {tree_path}")

# 
# BUOC 9: DU DOAN CHO TAP TEST CUA KAGGLE VA XUAT FILE SUBMISSION
# 
print("\n" + "=" * 60)
print("BUOC 9: DU DOAN CHO TAP TEST CUA KAGGLE")
print("=" * 60)

test_predictions = best_dt.predict(X_kaggle_test)
submission = pd.DataFrame({
    'PassengerId': df_test['PassengerId'],
    'Survived': test_predictions
})
sub_path = os.path.join(OUTPUT_DIR, "titanic_submission.csv")
submission.to_csv(sub_path, index=False)
print(f"[DA LUU] File submission Kaggle tai: {sub_path}")
print(submission.head())
print("\nHOAN TAT XU LY TITANIC DATASET!")
