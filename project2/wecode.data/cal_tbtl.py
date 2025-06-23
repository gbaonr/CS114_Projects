import pandas as pd

# Đọc các file csv
ck_df = pd.read_csv("ck-public.csv")
qt_df = pd.read_csv("qt-public.csv")
th_df = pd.read_csv("th-public.csv")

# Đổi tên các cột điểm cho dễ xử lý nếu cần
ck_df = ck_df.rename(columns={"hash": "hash", "CK": "CK"})
qt_df = qt_df.rename(columns={"hash": "hash", "diemqt": "QT"})
th_df = th_df.rename(columns={"hash": "hash", "TH": "TH"})

# Gộp 3 file theo cột "hash"
merged_df = pd.merge(qt_df, th_df, on="hash", how="outer")
merged_df = pd.merge(merged_df, ck_df, on="hash", how="outer")

merged_df["QT"] = pd.to_numeric(merged_df["QT"], errors='coerce')
merged_df["TH"] = pd.to_numeric(merged_df["TH"], errors='coerce')
merged_df["CK"] = pd.to_numeric(merged_df["CK"], errors='coerce')

# Tính TBTL
merged_df["TBTL"] = 0.1 * merged_df["QT"] + 0.6 * merged_df["TH"] + 0.3 * merged_df["CK"]


# Chọn 2 cột: hash và TBTL để xuất ra file mới
output_df = merged_df[["hash", "TBTL"]]
output_df.to_csv("tbtl-public.csv", index=False)

print("Đã tạo xong file tbtl-public.csv")
