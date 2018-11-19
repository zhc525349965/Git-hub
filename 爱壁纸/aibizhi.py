import requests
import json
from concurrent.futures import ThreadPoolExecutor
import pymongo
import os

def get_image_url(type,group_name,base_url,resources_urls):

    flag = True
    num = 0

    while flag:

        target_url = base_url.format(num*30)

        re = requests.get(target_url)

        json_content = json.loads(re.text)

        if type == 'image':

            if json_content['res']['vertical']:

                for i in (json_content['res']['vertical']):
                    resources_name = type + '/' + group_name + '/' +  str(i['id']) + '.jpeg'
                    resources_url = i['img']
                    resources_urls.append({'resources_name':resources_name,'resources_url':resources_url})
                print("类别：%s,子类别：%s，第%s页urls抓取完成"%(type,group_name,num+1))

            else:
                print("数据为空，停止抓取")
                flag = False

        if type == 'video':
            if json_content['res']['videowp']:

                for i in (json_content['res']['videowp']):
                    resources_name = type + '/' + group_name + '/' + str(i['id']) + '.mp4'
                    resources_url = i['video']
                    resources_urls.append({'resources_name':resources_name,'resources_url':resources_url})
                print("类别：%s,子类别：%s，第%s页urls抓取完成" % (type, group_name, num + 1))

            else:
                print("数据为空，停止抓取")
                flag = False
        num += 1

    print("类别：%s，子类别：%s爬取完成"%(type,group_name))

def save_to_mongo(collection,resources_url):
    collection.insert_one(resources_url)
    print("%s存储到Mongo"%(resources_url['resources_name']))

def download(resources_info):
    path = resources_info['resources_name']
    forder = os.path.dirname(path)
    parents_forder = os.path.dirname(forder)

    if not os.path.exists(parents_forder):
        print('创建文件夹%s'%parents_forder)
        os.mkdir(parents_forder)

    if not os.path.exists(forder):
        print('创建文件夹%s'%forder)
        os.mkdir(forder)

    re = requests.get(resources_info['resources_url']).content
    with open(resources_info['resources_name'], 'wb') as f:
        f.write(re)
    print("%s下载完成" % (resources_info['resources_name']))

if __name__ == "__main__":
    resources_urls = []
    aibizhi = {'image':{'美女':'http://service.aibizhi.adesk.com/v1/vertical/category/4e4d610cdf714d2966000000/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '动漫':'http://service.aibizhi.adesk.com/v1/vertical/category/4e4d610cdf714d2966000003/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '风景':'http://service.aibizhi.adesk.com/v1/vertical/category/4e4d610cdf714d2966000002/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '游戏':'http://service.aibizhi.adesk.com/v1/vertical/category/4e4d610cdf714d2966000007/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '文字':'http://service.aibizhi.adesk.com/v1/vertical/category/5109e04e48d5b9364ae9ac45/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '视觉':'http://service.aibizhi.adesk.com/v1/vertical/category/4fb479f75ba1c65561000027/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '情感':'http://service.aibizhi.adesk.com/v1/vertical/category/4ef0a35c0569795756000000/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '设计':'http://service.aibizhi.adesk.com/v1/vertical/category/4fb47a195ba1c60ca5000222/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '明星':'http://service.aibizhi.adesk.com/v1/vertical/category/5109e05248d5b9368bb559dc/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '物语':'http://service.aibizhi.adesk.com/v1/vertical/category/4fb47a465ba1c65561000028/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '艺术':'http://service.aibizhi.adesk.com/v1/vertical/category/4ef0a3330569795757000000/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '男人':'http://service.aibizhi.adesk.com/v1/vertical/category/4e4d610cdf714d2966000006/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '机械':'http://service.aibizhi.adesk.com/v1/vertical/category/4e4d610cdf714d2966000005/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '卡通':'http://service.aibizhi.adesk.com/v1/vertical/category/4e4d610cdf714d2966000004/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '城市':'http://service.aibizhi.adesk.com/v1/vertical/category/4fb47a305ba1c60ca5000223/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '动物':'http://service.aibizhi.adesk.com/v1/vertical/category/4e4d610cdf714d2966000001/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '运动':'http://service.aibizhi.adesk.com/v1/vertical/category/4ef0a34e0569795757000001/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                      '影视':'http://service.aibizhi.adesk.com/v1/vertical/category/4e58c2570569791a19000000/vertical?adult=0&appid=com.lovebizhi&appver=5.3&appvercode=56&channel=ipicture&first=1&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',

                      },
               'video':{'动漫新番':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e065e7bce72ce01371b1&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '网络红人':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e061e7bce72ce01371ae&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '游戏专区':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e009e7bce72ce0137170&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '热门推荐':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930df00e7bce72c3860daa2&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '其他资源':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e165e7bce72ce0137257&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '歌曲热舞':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e081e7bce72ce01371c8&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '娱乐明星':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e046e7bce72ce013719c&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '风景名胜':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e16ee7bce72ce013725f&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '热门影视':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e039e7bce72ce0137190&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',
                        '动物萌宠':'https://service.videowp.adesk.com/v1/aibizhi/videowp?appid=com.lovebizhi&appver=5.3&appvercode=56&category=5930e22ee7bce72ce01372f3&channel=ipicture&lan=zh-Hans-CN&limit=30&skip={}&sys_model=iPhone&sys_name=iOS&sys_ver=12.0',

                        },
               }

    ex = ThreadPoolExecutor(max_workers=10)

    for type,base_urls in aibizhi.items():
        for group_name,base_url in base_urls.items():
            ex.submit(get_image_url,type,group_name,base_url,resources_urls)

    ex.shutdown(wait=True)
    print("全部图片信息爬取完成")

    print("打开数据库")
    conn = pymongo.MongoClient()
    db = conn['aibizhi']
    collection = db['aibizhi']

    for resources_url in resources_urls:
        save_to_mongo(collection,resources_url)

    print("数据库存储完成")


    print('开始下载资源')
    download_resources_urls = []

    for i in  collection.find({}):
        download_resources_urls.append(i)

    print("一共需要下载%s个资源"%len(download_resources_urls))

    ex = ThreadPoolExecutor(max_workers=20)

    for resources_info in download_resources_urls:
        ex.submit(download,resources_info)
    ex.shutdown(wait=True)

    print("全部资源下载完成")

    print('关闭数据库')
    conn.close()