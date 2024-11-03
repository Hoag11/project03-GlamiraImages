import requests
import os
from urllib.parse import urlparse
from config import HEADERS
import logging
import re

# Cấu hình thư mục lưu ảnh
folder_path = 'images'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def standardlize_filename(filename):
    """Chuẩn hóa tên file bằng cách thay thế các ký tự không hợp lệ."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def generate_filename(url):
    parsed_url = urlparse(url)
    # Lấy đường dẫn và thay thế các ký tự không hợp lệ
    path = parsed_url.path.replace('/', '_')
    filename = f"{path}"
    filename_standardlized = standardlize_filename(filename)
    return filename_standardlized


def download_image(image_url):
    """Tải ảnh từ URL về thư mục chỉ định với tên file duy nhất."""
    try:
        response = requests.get(image_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            # Tạo tên file duy nhất
            name = generate_filename(image_url)
            img_name = os.path.join(folder_path, name)

            # Lưu ảnh vào file
            with open(img_name, 'wb') as f:
                f.write(response.content)
            logging.info(f"Đã tải xuống {img_name}")
        else:
            logging.error(f"Lỗi khi tải {image_url}: {response.status_code}")
    except Exception as e:
        logging.error(f"Lỗi khi tải {image_url}: {e}")
