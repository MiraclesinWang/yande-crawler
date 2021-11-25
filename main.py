import xml.etree.ElementTree as ET
from typing import List
import os
import multiprocessing
from multiprocessing import Pool

import requests
from tqdm import tqdm

url = 'https://yande.re/post.xml?limit=100&page={}&tags={}'
download_directory = './download'


def download(url: str):
    file_name = requests.utils.unquote(url[url.rfind('/') + 1:])
    file_id = file_name.split()[1]
    file_path = f'{download_directory}/{file_name}'
    if os.path.exists(file_path):
        return
    r = requests.get(url, stream=True)
    total = int(r.headers['content-length'])
    process_name = multiprocessing.current_process().name
    position = int(process_name[process_name.rfind('-') + 1:])
    progress_bar = tqdm(total=total, unit='B', unit_scale=True,
                        position=position, leave=None)
    progress_bar.set_description(file_id)
    with open(file_path, 'wb') as f:
        for data in r.iter_content(1024):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()


def main(*, tags: List[str] = None, page_limit: int = 0):
    tags = '' if tags is None else '+'.join(tags)
    max_page = page_limit if page_limit > 0 else float('inf')
    page = 1
    while page <= max_page:
        r = requests.get(url.format(page, tags))
        root = ET.fromstring(r.text)
        if len(root) == 0:
            break
        if page == 1:
            count = int(root.attrib['count'])
            main_progress = tqdm(total=count, position=0, desc='[main]')
        with Pool() as pool:
            image_urls = map(lambda child: child.attrib['file_url'], root)
            for iter in pool.imap(download, image_urls):
                main_progress.update(1)
        pool.join()
        page += 1


if __name__ == '__main__':
    if not os.path.exists(download_directory):
        os.mkdir(download_directory)
    main(tags=['izumi_sagiri'])
