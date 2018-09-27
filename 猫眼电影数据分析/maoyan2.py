import random
import pandas as pd
import time
import requests
import json

tomato = pd.DataFrame(columns=['date','score','city','comment','nick'])

for i in range(1,50):
    try:
        url ='http://m.maoyan.com/mmdb/comments/movie/1212592.json?_v_=yes&offset='+ str(i)
        html = requests.get(url=url).content
        data = json.loads(html)['cmts']
        for item in data:
            print(item)
            tomato = tomato.append({'date': item['time'],'city': item['cityName'],'score': item['score'],'comment': item['content'],'nick': item['nick']}, ignore_index=True)
        tomato.to_csv('西虹市首富4.csv', index=False,encoding='utf-8')
    except:
        continue