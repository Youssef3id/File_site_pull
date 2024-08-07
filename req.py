import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_file(url, folder):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        filename = os.path.join(folder, os.path.basename(urlparse(url).path))
        with open(filename, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def scrape_website(url, folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)

        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        # Save HTML
        html_path = os.path.join(folder, 'index.html')
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        # Save CSS
        css_folder = os.path.join(folder, 'css')
        if not os.path.exists(css_folder):
            os.makedirs(css_folder)
        for link in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(url, link['href'])
            download_file(css_url, css_folder)

        # Save images
        images_folder = os.path.join(folder, 'images')
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        for img in soup.find_all('img'):
            img_url = urljoin(url, img['src'])
            download_file(img_url, images_folder)
            
    except Exception as e:
        print(f"Error scraping {url}: {e}")

if __name__ == '__main__':
    website_url = input('Enter the URL of the website: ')
    folder_name = input('Enter the folder name to save files: ')
    scrape_website(website_url, folder_name)
    print("done")
