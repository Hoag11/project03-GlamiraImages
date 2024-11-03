from fake_useragent import UserAgent
import logging

# URL của trang chủ và sitemap
start_url = 'https://www.glamira.com/'
sitemap_url = 'https://www.glamira.com/sitemap.xml'

# Cấu hình User-Agent ngẫu nhiên
ua = UserAgent()
HEADERS = {
    'User-Agent': ua.random,
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)
