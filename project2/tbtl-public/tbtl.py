import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.abspath(os.path.join(base_dir, '..')) 

ck_path = os.path.join(project_root, 'ck-public', '33_features_no_corr_drop', 'results', 'xgb_272970_33.txt')
qt_path = os.path.join(project_root, 'qt-public', 'add_asignments_df', 'results', 'catb_273142_37.txt')
th_path = os.path.join(project_root, 'th-public', '33_features_no_corr_drop', 'results', 'xgb_272966_40.txt')
output_path = os.path.join(project_root, 'tbtl-public', 'tbtl.csv')

ck_df = pd.read_csv(ck_path)
qt_df = pd.read_csv(qt_path)
th_df = pd.read_csv(th_path)

ck_df = ck_df.rename(columns={"hash": "hash", "CK": "CK"})
qt_df = qt_df.rename(columns={"hash": "hash", "diemqt": "QT"})
th_df = th_df.rename(columns={"hash": "hash", "TH": "TH"})

merged_df = pd.merge(qt_df, th_df, on="hash", how="outer")
merged_df = pd.merge(merged_df, ck_df, on="hash", how="outer")

merged_df["QT"] = pd.to_numeric(merged_df["QT"], errors='coerce')
merged_df["TH"] = pd.to_numeric(merged_df["TH"], errors='coerce')
merged_df["CK"] = pd.to_numeric(merged_df["CK"], errors='coerce')

merged_df["TBTL"] = (0.20 * merged_df["QT"] + 0.40 * merged_df["TH"] + 0.40 * merged_df["CK"]).round(2)


output_df = merged_df[["hash", "TBTL"]]
output_df.loc[output_df['TBTL'] < 5, 'TBTL'] = 6
output_df.to_csv(output_path, index=False)

print("Đã tạo xong file tbtl-public.csv")
