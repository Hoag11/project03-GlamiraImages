from bs4 import BeautifulSoup
import requests
import os
import logging

start_url = ['https://www.glamira.com/sitemap.xml',
             'https://www.glamira.com/es/sitemap.xml']

header = {'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}

def fetch_url(url):
    response = requests.get(url, headers=header)
    return response.text

def get_urls(url):
    response = fetch_url(url)
    soup = BeautifulSoup(response, 'html.parser')
    urls = []
    for loc in soup.find_all('loc'):
        urls.append(loc.text)
    images = []
    for img in soup.find_all('img'):
        images.append(img['src'])
    return urls, images

def download_images(image_urls, download_folder='images'):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    for img_url in image_urls:
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(download_folder, os.path.basename(img_url))
            with open(img_name, 'wb') as handler:
                handler.write(img_data)
            logging.info(f'Successfully downloaded {img_name}')
        except Exception as e:
            logging.error(f'Failed to download {img_url}: {e}')

def main():
    for url in start_url:
        urls, images = get_urls(url)
        download_images(images)