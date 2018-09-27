import requests
import json
import csv

def save_info(content,title_list):
    content_list = []
    for s in title_list:
        try:
            sub_content = content[s]
        except:
            sub_content = ""
        content_list.append(sub_content)
    num = get_keywords_num(title_list,'nick')
    if content_list[num] not in user_list:
        with open('西红柿.csv', 'a', encoding='utf-8', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(content_list)
            user_list.append(content_list[num])
    else:
        pass

def create_csv(title_list):
    with open('西红柿.csv','w',encoding='utf-8',newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(title_list)

def get_content (url):
    r = requests.get(url)
    return json.loads(r.content)['cmts']

def get_keywords_num(title_list,target):
    for k,v in enumerate(title_list):
        if v == target:
            return k

if __name__ == "__main__":
    title_list = ['avatarurl','cityName','content','gender','id','nick','nickName','score','startTime','time','userId',
                  'userLevel','vipType']
    title_list = ['time', 'score','cityName', 'content', 'nick','startTime']
    user_list = []
    create_csv(title_list)
    base_url = "http://m.maoyan.com/mmdb/comments/movie/1212592.json?_v_=yes&offset="
    for i in range(1,1001):
        print('开始爬取第%s页'%i)
        url = base_url + str(i)
        content_list = get_content(url)
        for content in content_list:
            save_info(content,title_list)
    print("爬取完成")