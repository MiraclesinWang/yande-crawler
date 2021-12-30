import xml.etree.ElementTree as ET
from typing import List
import os

import threading
import requests
from tqdm import tqdm

os.environ['http_proxy'] = 'http://127.0.0.1:10809'
os.environ['https_proxy'] = 'http://127.0.0.1:10809'

template_url = 'https://yande.re/post.xml?limit=100&page={}&tags={}'
current_index = 0
sem = None
fail_lst = []

Lock = threading.Lock()


def download(url: str, save_name, progress_bar=None):
    file_name = requests.utils.unquote(url[url.rfind('/') + 1:])
    affix = os.path.splitext(file_name)[-1]
    print(f'Downloading \'{file_name}\'...')
    global current_index, sem
    if os.path.isdir(save_name):
        Lock.acquire()
        save_path = os.path.join(save_name, 'yande' + str(current_index).zfill(6) + affix)
        current_index += 1
        if progress_bar is not None:
            progress_bar.update(current_index)
        Lock.release()
    else:
        save_path = save_name
    try:
        r = requests.get(url, stream=True)
        # progress_bar = tqdm(total=total, unit='iB', unit_scale=True)
        with open(save_path, 'wb') as f:
            for data in r.iter_content(1024):
                f.write(data)
    except:
        global fail_lst
        fail_lst.append([url, save_path])
    sem.release()


def main(*, tags: List[str] = None, page_limit: int = int(1e9), download_directory: str='.', thread_limit = 10, score_threshold:int=0):
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    tags = '' if tags is None else '+'.join(tags)
    global current_index, sem, fail_lst
    current_index = 0
    fail_lst = []
    for page in range(page_limit):
        try:
            r = requests.get(template_url.format(page + 1, tags))
            root = ET.fromstring(r.text)

            progress_bar = tqdm(total=len(root)+current_index, unit='iB', unit_scale=True)
            sem = threading.Semaphore(4)
            sub_threads = []
            for child in root:
                if 'score' in child.attrib and int(child.attrib['score']) < score_threshold:
                    continue
                sub_threads.append(threading.Thread(target=download, args=(child.attrib['file_url'], download_directory, progress_bar)))
                sem.acquire()
                sub_threads[-1].start()
                # download(child.attrib['file_url'])
        except:
            if page_limit == int(1e9):
                break
            raise Exception('page limit exceeds number of accessible page')

    sem = threading.Semaphore(4)
    sub_threads = []
    if fail_lst:
        print('{:d} urls retrieval failed, retrying'.format(len(fail_lst)))
        for url, path in fail_lst:
            print(url, '\t', path)
        progress_bar = tqdm(total=len(fail_lst) + current_index, unit='iB', unit_scale=True)
        for _ in range(10):
            if not fail_lst:
                break
            retry_lst = fail_lst
            fail_lst = []
            for url, savepath in retry_lst:
                sub_threads.append(threading.Thread(target=download, args=(url, savepath, progress_bar)))
                sem.acquire()
                sub_threads[-1].start()

        if not fail_lst:
            print('after retrying, all images downloaded')
        else:
            print('after 10 rounds retrting, {:d} images still failed'.format(len(fail_lst)))
            for url, path in fail_lst:
                print(url, '\t', path)
                if path and os.path.exists(path):
                    os.remove(path)
                    

if __name__ == '__main__':
    main(tags=['loli', 'naked'], download_directory=r'D:\file\Pictures\loli', score_threshold=60)
