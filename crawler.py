import requests
from bs4 import BeautifulSoup
from config import sitemap_url, HEADERS
from urllib.parse import urljoin
import logging


def get_product_urls():
    """Lấy danh sách URL sản phẩm từ sitemap."""
    try:
        response = requests.get(sitemap_url, headers=HEADERS)
        response.raise_for_status()

        # Sử dụng parser XML với lxml
        soup = BeautifulSoup(response.text, features="xml")
        product_urls = [loc.text for loc in soup.find_all('loc')]
        logging.info(f"Tìm thấy {len(product_urls)} sản phẩm trong sitemap.")
        return product_urls
    except requests.RequestException as e:
        logging.error(f'Lỗi khi tải sitemap: {e}')
        return []


def get_image_urls(product_url):
    """Lấy tất cả URL ảnh từ tài liệu XML của trang sản phẩm."""
    try:
        response = requests.get(product_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        # Sử dụng BeautifulSoup với parser XML để phân tích cú pháp
        soup = BeautifulSoup(response.text, 'xml')

        # Tìm tất cả các URL ảnh trong sitemap sản phẩm
        image_urls = []
        for img in soup.find_all('image:loc'):
            img_url = img.text
            if img_url:
                full_img_url = urljoin(product_url, img_url)
                image_urls.append(full_img_url)

        logging.info(f"Tìm thấy {len(image_urls)} ảnh trong {product_url}")
        return image_urls
    except Exception as e:
        logging.error(f"Lỗi khi truy cập {product_url}: {e}")
        return []
