import requests
import time
import json
import pymongo

def get_news_info():
    time_timeStamp = (str(int(time.time())))

    times = 5
    while times > 0:
        url = 'https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=blockchain-channel&client=pc&cursor=' + str(
            time_timeStamp) + '&limit=20'

        content = requests.get(url)

        content_json = json.loads(content.content)
        news_contents = (content_json['data']['items'])
        for news_content in news_contents:
            item = {}
            title = news_content['title']

            display_time = news_content['display_time']
            timeArray = time.localtime(display_time)
            format_time = time.strftime("%Y:%m:%d %H:%M:%S", timeArray)

            content_all = news_content['content_text'].strip() + news_content['content_more'].strip()

            item['time'] = format_time
            item['title'] = title
            item['content'] = content_all
            save_info(item)

        time_timeStamp = (content_json['data']['items'][-1]['display_time'])

        times -= 1
        time.sleep(3)



def save_info(news_info):
    conn = pymongo.MongoClient()
    db = conn['wallstreetcn']
    collections = db['wallstreetcn']

    collections.insert_one(news_info)
    conn.close()

    print("%s存储完成"%news_info)



if __name__ == "__main__":
    get_news_info()