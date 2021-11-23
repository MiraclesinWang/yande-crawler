import urllib.request
import urllib.parse
import requests
import re
import os
import threading
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# post-list-posts

# https://yande.re/post?page=2&tags=izumi_sagiri

pic_finished = 0

def url_traverse(tag, page_num):
    url_lst = ['https://yande.re/post?tags='+tag]


    if page_num:
        url_lst = url_lst + ['https://yande.re/post?page='+str(i)+'&tags='+tag for i in range(2, page_num+1)]
        return url_lst

    req = urllib.request.Request(url=url_lst[0], headers=headers, method='GET')
    try:
        response = urllib.request.urlopen(req, timeout=40)
    except:
        raise Exception('tag not founded')

    dex = 2
    while True:
        url_lst.append('https://yande.re/post?page='+str(dex)+'&tags='+tag)
        req = urllib.request.Request(url=url_lst[-1], headers=headers, method='GET')
        try:
            response = urllib.request.urlopen(req, timeout=40)
        except:
            break
        dex+=1
    return url_lst

def Get_img_urls(url_lst):
    img_urls = []
    while len(url_lst):
        url_now = url_lst[0]
        req = urllib.request.Request(url=url_now, headers=headers, method='GET')
        url_lst.pop(0)
        try:
            response = urllib.request.urlopen(req, timeout=40)
            text = response.read().decode('utf-8')
            print('Read success:', url_now)
        except:
            url_lst.append(url_now)
            continue
        # pic_lst_str = re.compile("(?<=post-list-posts).+?\.(?=</ul>)", re.DOTALL)
        # img_id = re.compile('(?<=<img id="img" src=").+?\.(jpg|png|jpeg|tif|webp|gif|bmp|eps|pcx|tga|svg|psd)',
        #                     re.DOTALL)

        # img_url_str = re.compile("(?<=Preload\.preload\(').+?(?='\))")

        # img_file_str = re.compile("(?<=file_url:\").+?(?=\")")
        img_file_str = re.compile("(?<=file_url).+?(?=is_shown_in_index)")
        sub_img_urls = re.findall(img_file_str, text)

        sub_img_urls = [url[3:-3] for url in sub_img_urls]

        print("get {:d} img urls, {:d} pages left".format(len(sub_img_urls), len(url_lst)))

        img_urls += sub_img_urls

    return img_urls

def one_image_download(output_path, img_url):
    fail_cnt = 0
    while True:
        try:
            fp = open(output_path, 'wb')
            fp.write((urllib.request.urlopen(img_url)).read())
            # fp.write(requests.get(img_url, timeout=120, headers=headers).content)
            fp.close()

            global pic_finished
            pic_finished = pic_finished + 1

            print("download success, {:d} images downloaded, url: {:s}, path: {:s}".format(pic_finished, img_url, output_path))
            break
        except Exception as E:
            try:
                if int(E.code) == 429:
                    fail_cnt = fail_cnt + 1
                    time.sleep(min(10*fail_cnt, 60))
            except:
                print("download failed", E, "url:", img_url)

def Multi_process_download(img_urls, output_dir, prefix='', start_dex=0):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    sub_threads = []
    for i in range(len(img_urls)):
        img_url = img_urls[i]
        affix = os.path.splitext(img_url)[-1]
        file_name = prefix + str(start_dex+i).zfill(6) + affix
        sub_threads.append(threading.Thread(target=one_image_download, args=(os.path.join(output_dir, file_name), img_url)))
        sub_threads[-1].start()

    for i in sub_threads:
        i.join()
    print('download finished')

def download_imgs(img_urls, output_dir, prefix='', start_dex=0):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    while len(img_urls):
    # for img_url in img_urls:
        img_url = img_urls[0]
        img_urls.pop(0)

        affix = os.path.splitext(img_url)[-1]

        file_name = prefix + str(start_dex).zfill(6) + affix
        # print(file_name, img_url)

        try:
            fp = open(os.path.join(output_dir, file_name), 'wb')
            # fp.write((urllib.request.urlopen(img_url)).read())
            fp.write(requests.get(img_url, timeout=10, headers=headers).content)
            fp.close()
            start_dex += 1


            print("download success, {:d} images left, file: {:s}, url: {:s}".format(len(img_urls), file_name, img_url))
        except:
            img_urls.append(img_url)

    return

def Pic_crawler(tag, page_num=0, output_dir='.', prefix='', start_dex=0):
    url_lst = url_traverse(tag, page_num)
    img_urls = Get_img_urls(url_lst)
    global pic_finished
    pic_finished = 0
    Multi_process_download(img_urls, output_dir, prefix, start_dex)
    # download_imgs(img_urls, output_dir, prefix, start_dex)

if __name__ == '__main__':
    # Pic_crawler('izumi_sagiri', 16, r'D:\file\Pictures\纱雾酱\yande', 'yande')

