import requests
import re
from bs4 import BeautifulSoup
import os
import json

def save_car_brand_icon(car_brand_icon_url,car_brand,forder):
    #拼接图片url
    url = "http:" + car_brand_icon_url

    #拼接图片名称
    name = car_brand + '.png'

    #判断要存储的文件夹是否存在
    if not os.path.exists(os.path.join(forder,'CarImage')):
        os.mkdir(os.path.join(forder,'CarImage'))

    #判断文件名是否存在
    path = os.path.join(forder,'CarImage',name)
    if os.path.exists(path):
        print("文件已经存在")
    else:
        r = requests.get(url)
        with open(path,'wb') as f :
            f.write(r.content)
            print('%s已经存储完成'%path)

def save_carinfo(url,forder):
    #获取reponse，并生成BeautifulSoup对象
    r = requests.get(url)
    content = r.content
    content_string = content.decode('ANSI')
    soup = BeautifulSoup(content_string)

    #寻找所有A标签
    find_a = soup.find_all(['a'])

    #车辆品牌正则
    pattern_brand = re.compile(r'<a href="//car.autohome.com.cn/(price|pic)/brand-[^\D]*.html#pvareaid=[^\s]+">(.*)</a>')

    #车辆型号正则
    pattern_model = re.compile(r'<a (class="greylink" )?href="//www.autohome.com.cn/[^\s]+/#levelsource=[^\s]+&amp;pvareaid=[^\s]+">(.*)</a>')

    #车辆品牌图片正则
    pattern_img = re.compile(r'<img height="50" src="(.*)" width="50"/>')

    #从a标签列表中匹配正则
    for a in find_a:
        #将a转换成字符串
        a = str(a)

        #获取车辆品牌图片url，存储url
        try:
            car_brand_icon_url = pattern_img.search(a)[1]
        except:
            pass

        #获取车辆品牌名称，
        try:
            s = pattern_brand.search(a)[2]
            #如果不是以“<”开头，则是我们想要的车辆品牌名称。调用保照片方法。
            if not s.startswith('<'):
                car_brand = s
                car_info[car_brand] = []
                save_car_brand_icon(car_brand_icon_url,car_brand,forder)
        except:
            pass

        #获取车辆型号，并以字典形式存储在car_info中
        try:
            s = pattern_model.search(a)[2]
            car_info[car_brand].append(s)
        except:
            pass
    print("爬取完一页")
    return car_info

if __name__ == "__main__":
    #车辆信息存储，最终按照字典方式存储。格式[品牌1：型号1，型号2,；品牌2：型号1，型号2]
    car_info = {}
    #中间变量，存储车辆品牌，存储文件时用到
    car_brand = ""

    baseurl = "https://www.autohome.com.cn/grade/carhtml/"
    #获取当前目录
    forder = os.getcwd()

    #将65-90转换成A-Z，并拼接URL，调用save_carinfo方法
    for a in range(65,91):
        url = baseurl+str(chr(a))+".html"
        car_info = save_carinfo(url,forder)

    #将返回数据写入文件
    with open('car.text','w',encoding='utf-8 ') as f:
        file_content = json.dumps(car_info)
        f.write(file_content)