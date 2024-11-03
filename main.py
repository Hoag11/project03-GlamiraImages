import downloader
import crawler
import logging
import concurrent.futures


def main():
    logging.info("Bắt đầu quy trình crawl.")
    product_urls = crawler.get_product_urls()

    if not product_urls:
        logging.warning("Không có sản phẩm nào để crawl.")
        return

    all_image_urls = []
    for product_url in product_urls:
        logging.info(f"Đang xử lý sản phẩm: {product_url}")
        image_urls = crawler.get_image_urls(product_url)

        if not image_urls:
            logging.warning(f"Không tìm thấy ảnh nào trong sản phẩm: {product_url}")
            continue

        all_image_urls.extend(image_urls)

    # Sử dụng ThreadPoolExecutor để tải ảnh song song với số lượng worker tăng
    max_workers = 15  # Số lượng worker có thể điều chỉnh theo tài nguyên hệ thống
    logging.info(f"Bắt đầu tải xuống {len(all_image_urls)} ảnh với {max_workers} worker.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(downloader.download_image, all_image_urls)

    logging.info("Quy trình crawl hoàn tất.")


if __name__ == '__main__':
    main()
