#!/usr/bin/python3
import requests
import re
from time import sleep

# сounter - число, с которого должна начинаться нумерация файлов
counter = 0

def get_cookies():
    cookies = {}
    with open("cookies.txt", 'r') as f:
        for line in f:
            if not line.startswith("#") and len(line) > 1:
                line_fields = line.strip().split('\t')
                cookies[line_fields[5]] = line_fields[6]
    return cookies

def download_file(url, cookies):
    """
    Скачивает файл по ссылке.
    """
    sleep(0.2)
    try:
        resp = requests.get(url, cookies=cookies)
        global counter

        if resp.status_code == 200:
            with open(f"torrents/file{counter}.torrent", 'wb') as file:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            print(f"torrents/file{counter}.torrent successfully downloaded")
            counter += 1
        else:
            print("failed to download")
    
    except:
        print("что-то пошло по пизде, но в целом похуй")



def process_page(page_url, cookies, threshold=1000):
    """
    Принимает ссылку на страницу, находит на этой странице все ссылки на .torrent файлы,
    проверяет, что у этих файлов количество скачиваний >= threshold, скачивает каждый
    .torrent в директорию ./torrents/
    """
    
    try:
        resp = requests.get(page_url, cookies=cookies)
    
        urls = re.findall("<a class=\"small tr-dl dl-stub\" href=.*/a>", resp.text)
        for i in range(len(urls)):
            urls[i] = "https://rutracker.net/forum/" + urls[i][37:53]
    
        downloads = re.findall("<td class=\"row4 small number-format\">.*</td>", resp.text)
        for i in range(len(downloads)):
            downloads[i] = downloads[i][37:-5]
    
        result = tuple(zip(urls, downloads))
    
        for link in result:
            if int(link[1]) >= threshold:
                download_file(link[0], cookies)
    except:
        print("error")

def iter_urls(path, cookies):
    """
    Принимает путь к файлу, в котором записаны ссылки на страницы (по одной ссылке на строку)
    """
    with open(path, 'r') as f:
        for line in f:
            if len(line) > 2:
                print(line)
                process_page(line.strip(), cookies=cookies)

if __name__ == "__main__":
    cookies = get_cookies()
    iter_urls("urls.txt", cookies)

