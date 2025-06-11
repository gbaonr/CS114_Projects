#!pip install pyheif pillow -q

import os
import shutil
import random
from collections import defaultdict
from PIL import Image, UnidentifiedImageError
import pyheif
import uuid

# Hàm chuyển đổi .heic sang .jpeg
def convert_heic_to_jpeg(heic_path, jpeg_path):
    try:
        heif_file = pyheif.read(heic_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data, 
            "raw", 
            heif_file.mode, 
            heif_file.stride,
        )
        image.save(jpeg_path, format="JPEG")
    except Exception as e:
        print(f"Lỗi chuyển đổi .heic: {heic_path} — {e}")

# Hàm kiểm tra ảnh hợp lệ
def is_valid_image(path):
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False

# Hàm mã hóa tên tệp để đảm bảo duy nhất
def encode_filename(original_name, split, digit, counter, ext):
    # Lấy phần tên cơ bản và chuẩn hóa
    base_name = os.path.splitext(original_name)[0].lower().replace('x', '').replace('d', '')
    # Tạo tên mới với tiền tố split, digit và số thứ tự để tránh trùng lặp
    unique_id = f"{counter:04d}"  # Số thứ tự 4 chữ số (0001, 0002, ...)
    return f"{split}_{digit}_{base_name}_{unique_id}{ext}"

random.seed(42)
input_path = '/kaggle/input/handwritten-train-cs114/data'
output_path = 'data/digits_data'
train_ratio = 0.8

# Tạo thư mục train và val
for split in ['train', 'val']:
    for digit in range(10):
        os.makedirs(os.path.join(output_path, split, str(digit)), exist_ok=True)

# Thu thập tất cả file theo digit
digit_files = defaultdict(list)
for folder in os.listdir(input_path):
    folder_path = os.path.join(input_path, folder)
    
    if not os.path.isdir(folder_path):
        continue

    for sub_folder in os.listdir(folder_path):
        sub_folder_path = os.path.join(folder_path, sub_folder)
        
        for file in os.listdir(sub_folder_path):
            if file[0].isdigit() and file[1] == '_':
                digit = file[0]
                digit_files[digit].append(os.path.join(sub_folder_path, file))

# Theo dõi tên tệp để phát hiện trùng lặp
used_filenames = set()

# Phân chia và xử lý file
for digit, files in digit_files.items():
    random.shuffle(files)
    split_idx = int(len(files) * train_ratio)
    train_files = files[:split_idx]
    val_files = files[split_idx:]

    # Biến đếm để tạo mã định danh duy nhất
    counter = 1

    for split, split_files in [('train', train_files), ('val', val_files)]:
        for file_path in split_files:
            try:
                ext = os.path.splitext(file_path)[-1].lower()
                file_name = os.path.basename(file_path)
                # Mã hóa tên tệp
                new_name = encode_filename(file_name, split, digit, counter, ext)
                counter += 1  # Tăng số thứ tự để đảm bảo tên tệp duy nhất
                dst_file = os.path.join(output_path, split, digit, new_name)

                # Kiểm tra trùng lặp
                if new_name in used_filenames:
                    print(f"🛑 Cảnh báo: Tên tệp trùng lặp '{new_name}' tại {file_path}")
                    continue
                used_filenames.add(new_name)

                if ext == '.heic':
                    convert_heic_to_jpeg(file_path, dst_file)
                else:
                    shutil.copy(file_path, dst_file)

                if not is_valid_image(dst_file):
                    os.remove(dst_file)
                    print(f"🗑️ Ảnh lỗi bị loại ({split}): {file_path}")
                # else:
                #     print(f"✅ Xử lý thành công: {dst_file}")
                # print(dst_file)
                
            except Exception as e:
                print(f"🛑 Lỗi xử lý ảnh ({split}): {file_path} — {e}")

print("Stratified train and validation sets created!")

# Tạo file .zip
import zipfile

data_folder = 'data/digits_data'
output_zip = 'digits_data.zip'

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, data_folder)
            zipf.write(file_path, os.path.join('digits_data', relative_path))

print(f"Folder {data_folder} has been zipped into {output_zip}!")

# Kiểm tra file .zip
print("Kiểm tra file .zip...")
try:
    with zipfile.ZipFile(output_zip, 'r') as zipf:
        zipf.testzip()
        print("✅ File .zip hợp lệ, không có lỗi!")
except zipfile.BadZipFile:
    print("File .zip bị lỗi, hãy kiểm tra lại!")