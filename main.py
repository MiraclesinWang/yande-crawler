import xml.etree.ElementTree as ET
from typing import List
import os

import requests
from tqdm import tqdm

url = 'https://yande.re/post.xml?limit=100&page={}&tags={}'
download_directory = './download'


def download(url: str):
    file_name = requests.utils.unquote(url[url.rfind('/') + 1:])
    print(f'Downloading \'{file_name}\'...')
    r = requests.get(url, stream=True)
    total = int(r.headers['content-length'])
    progress_bar = tqdm(total=total, unit='iB', unit_scale=True)
    with open(f'{download_directory}/{file_name}', 'wb') as f:
        for data in r.iter_content(1024):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()


def main(*, tags: List[str] = None, page_limit: int = 1):
    tags = '' if tags is None else '+'.join(tags)
    for page in range(page_limit):
        r = requests.get(url.format(page + 1, tags))
        root = ET.fromstring(r.text)
        for child in root:
            download(child.attrib['file_url'])


if __name__ == '__main__':
    if not os.path.exists(download_directory):
        os.mkdir(download_directory)
    main(tags=['izumi_sagiri', 'naked'])
