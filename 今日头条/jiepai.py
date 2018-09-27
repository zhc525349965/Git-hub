import requests
from multiprocessing.pool import Pool
import os
import re

def get_return_data(offset,keyword="街拍"):
    """
    :param offset: 偏移量
    :param keyword: 搜索关键字
    :return: 搜索结果页面【data】数据
    """
    url = "https://www.toutiao.com/search_content/"
    params = {
        "offset":offset,
        "format":"json",
        "keyword":keyword,
        "autoload":"true",
        "count":20,
        "cur_tab":1,
        "from":"search_tab",
    }
    r = requests.get(url,params=params)
    return r.json().get('data')

def get_image_info(data):
    for item in data:
        if item.get('cell_type') is not None:
            continue
        if not item.get("has_gallery"):
            continue
        title = item.get('title')
        article_url = item.get('article_url')
        yield {
            'title': title,
            "article_url":article_url.replace("http://toutiao.com/group/","https://www.toutiao.com/a"),
        }

def save_image(item):

    title = item['title']
    article_url = item['article_url'] + "#p="

    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    img_path = 'img' + os.path.sep + title
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    img_id_list = get_detail_image(article_url)

    for img_id in img_id_list:
        start_url = "http://p3.pstatp.com/origin/pgc-image/"
        img_url = start_url+img_id
        file_name = img_path + os.path.sep + img_id + ".jpg"
        content = requests.get(img_url,headers=headers).content

        with open(file_name,"wb") as f:
            f.write(content)
            print("%s download complete"%file_name)

def get_detail_image(url):
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    r = requests.get(url,headers=headers)
    text = r.text.replace("\\","")
    pattern_image_url = re.compile(r'"url":"(.*?)"')
    image_url = pattern_image_url.findall(text)
    image_id = []
    for url in image_url:
        try:
            image_id.append(url.split("/pgc-image/")[1])
        except:
            pass
    image_id = set(image_id)
    return image_id

def main(offset):
    return_data = get_return_data(offset)
    image_list = get_image_info(return_data)
    for item in image_list:
        save_image(item)

if __name__ == "__main__":
    pool = Pool()
    GROUP_START = 0
    GROUP_END = 7
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()