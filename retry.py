import re
import logging
import downloader
import crawler
import concurrent.futures


retry_log_file = 'retry.log'

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Tạo logger riêng cho retry
retry_logger = logging.getLogger('retry_logger')
retry_handler = logging.FileHandler(retry_log_file)
retry_handler.setLevel(logging.WARNING)
retry_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
retry_logger.addHandler(retry_handler)


def take_error_url(log_file='crawler.log'):
    """Lấy danh sách các link mà không tìm được ảnh."""
    links = set()
    warning_pattern = re.compile(r'WARNING.*(https?://[^\s]+)')
    try:
        with open(log_file, 'r') as f:
            for line in f:
                match = warning_pattern.search(line)
                if match:
                    links.add(match.group(1))
    except FileNotFoundError:
        logging.error(f'File log "{log_file}" không tồn tại.')
    except Exception as e:
        logging.error(f'Lỗi khi đọc file log: {e}')
    return list(links)


def take_error_image(log_file='crawler.log'):
    """Lấy danh sách các URL ảnh bị lỗi từ file log."""
    failed_images = set()
    error_pattern = re.compile(r'Lỗi khi tải (https?://[^\s]+)')

    try:
        with open(log_file, 'r') as f:
            for line in f:
                match = error_pattern.search(line)
                if match:
                    failed_images.add(match.group(1))
    except FileNotFoundError:
        logging.error(f'File log "{log_file}" không tồn tại.')
    except Exception as e:
        logging.error(f'Lỗi khi đọc file log: {e}')

    logging.info(f"Tìm thấy {len(failed_images)} URL ảnh bị lỗi.")
    return list(failed_images)


def retry_failed_links(failed_urls, failed_images, max_retries=3):
    """Retry tải các URL hoặc hình ảnh thất bại, với số lần retry giới hạn."""
    for attempt in range(max_retries):
        logging.info(f"Bắt đầu retry lần {attempt + 1}/{max_retries}")

        # Retry lấy ảnh từ các URL thất bại
        if failed_urls:
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                results = executor.map(crawler.get_image_urls, failed_urls)

                # Xác định các URL thành công và thất bại
                success_urls = [url for url, result in zip(failed_urls, results) if result]
                failed_urls = [url for url in failed_urls if url not in success_urls]

        # Retry tải các ảnh thất bại
        if failed_images:
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                results = executor.map(downloader.download_image, failed_images)

                # Xác định các ảnh tải thành công và thất bại
                success_images = [img for img, result in zip(failed_images, results) if result]
                failed_images = [img for img in failed_images if img not in success_images]

        # Kiểm tra nếu không còn URL hoặc ảnh nào để retry
        if not failed_urls and not failed_images:
            logging.info("Tất cả URL và ảnh đã được xử lý thành công.")
            return

    # Ghi lại các URL và ảnh vẫn thất bại sau khi retry
    for url in failed_urls:
        retry_logger.warning(f'Không tìm thấy ảnh trong {url}')
    for img_url in failed_images:
        retry_logger.warning(f'Lỗi khi tải {img_url}')
    logging.info(f"Các URL và ảnh không thành công đã được ghi lại trong {retry_log_file}.")


def main():
    logging.info("Bắt đầu quy trình xử lý link ảnh không tìm được ảnh.")
    failed_urls = take_error_url()
    failed_images = take_error_image()

    # Retry các URL và ảnh thất bại với giới hạn số lần thử
    retry_failed_links(failed_urls, failed_images)

    logging.info("Quy trình xử lý hoàn tất.")


if __name__ == '__main__':
    main()
