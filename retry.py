import re
import logging
import downloader
import crawler
import concurrent.futures

def take_error_url(log_file='crawler.log'):
    """lấy danh sách các link mà không tìm được ảnh"""
    links = []
    warning_pattern = re.compile(r'WARNING.*(https?://[^\s]+)')
    try:
        with open(log_file, 'r') as f:
            for line in f:
                match = warning_pattern.search(line)
                if match:
                    links.append(match.group(1))
    except FileNotFoundError:
        logging.error(f'File log "{log_file}" không tồn tại.')
    except Exception as e:
        logging.error(f'Lỗi khi đọc file log: {e}')
    return links

def take_error_image(log_file='crawler.log'):
    """Lấy danh sách các URL ảnh bị lỗi từ file log."""
    failed_image = set()  # Sử dụng set để đảm bảo không có URL trùng lặp
    error_pattern = re.compile(r'Lỗi khi tải (https?://[^\s]+)')

    try:
        with open(log_file, 'r') as f:
            for line in f:
                match = error_pattern.search(line)
                if match:
                    failed_image.add(match.group(1))  # Sử dụng add() với set để thêm URL
    except FileNotFoundError:
        logging.error(f'File log "{log_file}" không tồn tại.')
    except Exception as e:
        logging.error(f'Lỗi khi đọc file log: {e}')

    logging.info(f"Tìm thấy {len(failed_image)} URL ảnh bị lỗi.")
    return list(failed_image)  # Trả về danh sách để dễ xử lý sau này

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Bắt đầu quy trình xử lý link ảnh không tìm được ảnh.")
    max_workers = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        failed_urls = take_error_url()
        executor.map(crawler.get_image_urls, failed_urls)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Bắt đầu quy trình xử lý ảnh bị lỗi.")
    max_workers = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        failed_images = take_error_image()
        executor.map(downloader.download_image, failed_images)

    logging.info("Quy trình xử lý ảnh bị lỗi hoàn tất.")

if __name__ == '__main__':
    main()
