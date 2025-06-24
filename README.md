# 🎓 **Đồ án cuối kỳ môn Học Máy - CS114 UIT**

Repository này chứa toàn bộ nội dung đồ án cuối kỳ của nhóm trong môn **CS114 - Học Máy** tại UIT. Đồ án bao gồm hai phần chính:

- **Phần 1:** Nhận diện chữ số viết tay (Handwritten Digits Classification)
- **Phần 2:** Dự đoán điểm dựa trên dữ liệu Wecode (Scores Prediction Based on Wecode Practical Score)

---

## 🖊️ **Phần 1: Nhận diện chữ số viết tay**

### 📌 **Bài toán**

Đây là một bài toán kinh điển trong lĩnh vực **Thị giác máy tính (Computer Vision)** và **Học máy (Machine Learning)**: xây dựng một hệ thống có khả năng phân loại chính xác các chữ số từ **0 đến 9** viết tay trong các ảnh đầu vào.

### 📁 **Dữ liệu**

- **Tập huấn luyện (\~8.000 ảnh):**\
  Được sinh viên trong lớp tự tạo thủ công và tổng hợp từ nhiều repo GitHub khác nhau.\
  Mỗi ảnh chứa một chữ số duy nhất (0–9), tên file có định dạng:\
  `<chữ_số_từ_0_đến_9>_<chuỗi_bất_kỳ>.<định_dạng>`\
  Ví dụ: `5_nguyenanhtuan.jpg`, `0_img001.png`

- **Tập kiểm tra:**\
  Gồm hai bộ:

  - ✅ **2K Test Set**: 2.939 ảnh (không có nhãn)
  - ✅ **10K Test Set**: 9.974 ảnh (không có nhãn)

  Tên file là mã định danh ngẫu nhiên, ví dụ: `d9cc0b1ef1...jpg`.

- **Nguồn dữ liệu:**

  - Tập train: [Kaggle Handwritten TL Dataset](https://www.kaggle.com/datasets/nahrixt/handwritten-tl)
  - Tập test 2k: [Kaggle Handwritten Test 2k](https://www.kaggle.com/datasets/nahrixt/handwritten-test-cs114)
  - Tập test 10k: [Kaggle Handwritten Test 10k](https://www.kaggle.com/datasets/nahrixt/handwritten-test-10k)

### 🎯 **Yêu cầu đầu ra**

Sinh viên cần xuất kết quả dự đoán dưới định dạng:

```
<file_name>,<chữ_số_dự_đoán>
```

Ví dụ:

```
d9cc0b1ef18554757e3ff3ed507f4e7e.jpg,1
3da8f9b5d148bf172d6faa1410746e86.jpg,2
```

### 📂 **Cấu trúc thư mục**

```
project1/
├── Model_X/
│   ├── version_Y/
│   │   ├── <file-name>.ipynb       # Notebook huấn luyện model
│   │   ├── predict_2k_<id>_<score>.txt  # Kết quả dự đoán 2k
│   │   ├── predict_10k_<id>_<score>.txt # Kết quả dự đoán 10k
│   │   ├── train_log.txt           # Log huấn luyện
├── top.py                          # Script tổng hợp kết quả
├── format_train_data.py            # Script tách tập train/val
```

- **top.py:** Nhóm dùng để liệt kê top X kết quả:

  ```bash
  python top.py --top <X>
  ```

- **format_train_data.py:** Nhóm dùng để phân chia dữ liệu train-val cho 1 vài versions.

---

## 📈 **Phần 2: Dự đoán điểm dựa trên dữ liệu Wecode**

### 📌 **Bài toán**

Xây dựng mô hình dự đoán điểm số cho sinh viên (điểm TH, quá trình, cuối kỳ, TBTL) dựa vào dữ liệu nộp bài từ hệ thống **Wecode**.

### 📁 **Dữ liệu**

Dữ liệu đầu vào gồm 4 file CSV:

- **anonimized.csv:** Thông tin chi tiết về các lần nộp bài
- **qt-public.csv:** Điểm quá trình thật
- **th-public.csv:** Điểm thực hành thật
- **ck-public.csv:** Điểm cuối kỳ thật

### 🎯 **Yêu cầu đầu ra**

Dự đoán lưu dưới định dạng:

```
<username>,<điểm_dự_đoán>
```

Ví dụ:

```
4c9a347f2988f1dd733c2098b9f6f15d,7.25
92ac6aeea0ad9814089c921e32c4e2f9,8.50
```

### 📂 **Cấu trúc thư mục**

```
project2/
├── ck-public/
│   ├── 33_features_no_corr_drop/ # ở cấp folder này, có folder là add_assignment_df, là kết quả được cải thiện sau vấn đáp
│   │    ├── notebook_ck.ipynb
│   │    └── results/
│   │        ├── <model>_<id>_<score>.txt #  # có 2 hoặc nhiều model , ví dụ : catb_273142_37.txt
│   ├──... # còn nhiều folder trong ck-public ở đây chỉ ví dụ 33_features_no_corr_drop
│
├── th-public/
│   ├── 33_features_no_corr_drop/
│   │    ├── notebook_th.ipynb
│   │    └── results/
│   │        ├── <model>_<id>_<score>.txt
│   ├──...
│
├── qt-public/
│   ├── 33_features_no_corr_drop/
│   │   ├── notebook_qt.ipynb
│   │   └── results/
│   │        ├── <model>_<id>_<score>.txt
│   ├──...
│
├── tbtl-public/
│   ├── 22_features_no_corr_drop/
│   │    ├── notebook_tbtl.ipynb
│   │    └── results/
│   │        ├── <model>_<id>_<score>.txt
│   ├──tbtl.csv # file tbtl được tính ra từ kết quả tốt nhất từ CK, TH, QT
│   ├──tbtl.py # file .py để tính ra file tbtl.csv
│   ├──...
│
├── wecode.data/
│    ├── anonymized.csv
│    ├── ck-public.csv
│    ├── th-public.csv
│    ├── qt-public.csv
│    ├── tbtl-public.csv # điểm tbtl được tình từ 3 file trên
│    ├── cal_tbtl.py # file .py để tính ra file tbtl-public.csv
│
└── test / # folder chứa những notebook test, hoặc những kết quả được test , không chính thức

```
