import requests
import json
import time
import pymongo

def _36kr():

    base_url = 'https://36kr.com/lapi/info-flow/newsflash_columns/newsflashes?per_page=20{}'

    re = requests.get(base_url)
    json_content = json.loads(re.text)

    code = json_content['code']
    itmes = (json_content['data']['items'])
    page = 0

    while code == 0 and page <= 100:

        for i in itmes:
            news_info = {}
            news_info['id'] = i['id']
            news_info['title'] = i['title']
            news_info['description'] = i['description']
            news_info['news_url'] = i['news_url']

            save(news_info)

            time.sleep(0.2)

        b_id= '&b_id=' + str(itmes[-1]['id'])
        url = base_url.format(b_id)

        re = requests.get(url)
        json_content = json.loads(re.text)

        code = json_content['code']
        itmes = (json_content['data']['items'])

        page += 1

        time.sleep(5)

def save(news_info):
    conn = pymongo.MongoClient()
    db = conn['36kr']
    collection = db['news']

    collection.insert_one(news_info)

    print('id：%s 存储完成'%(news_info['id']))

if __name__ == '__main__':
    _36kr()