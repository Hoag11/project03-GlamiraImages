import requests
import os
import hashlib
from config import HEADERS
import logging

# Cấu hình thư mục lưu ảnh
folder_path = 'images'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


def generate_unique_filename(url):
    """Tạo tên file duy nhất từ URL bằng mã băm SHA-256."""
    hash_object = hashlib.sha256(url.encode())
    hex_dig = hash_object.hexdigest()
    extension = os.path.splitext(url)[-1]  # Lấy phần mở rộng từ URL gốc (nếu có)
    if not extension or len(extension) > 5:  # Nếu không có hoặc phần mở rộng quá dài, mặc định là .jpg
        extension = '.jpg'
    return f"{hex_dig}{extension}"


def download_image(image_url):
    """Tải ảnh từ URL về thư mục chỉ định với tên file duy nhất."""
    try:
        response = requests.get(image_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            # Tạo tên file duy nhất
            unique_name = generate_unique_filename(image_url)
            img_name = os.path.join(folder_path, unique_name)

            # Lưu ảnh vào file
            with open(img_name, 'wb') as f:
                f.write(response.content)
            logging.info(f"Đã tải xuống {img_name}")
        else:
            logging.error(f"Lỗi khi tải {image_url}: {response.status_code}")
    except Exception as e:
        logging.error(f"Lỗi khi tải {image_url}: {e}")
