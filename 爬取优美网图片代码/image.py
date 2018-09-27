import re
import requests
import time,os
from bs4 import BeautifulSoup

def create_dir(path):
    '''
    :param path: 给定一个文件名
    :return: 在./image下创建文件夹并返回路径
    '''
    url = "./image/" + path
    #判断当前文件夹是否存在
    if os.path.exists(url):
        print("文件夹已经存在")
    else:
        os.makedirs(url)
        print("%s创建成功"%url)
    #将当前文件夹作为路径返回
    return url

def get_image(url,forder):
    '''
    :param url: 图集URL
    :param forder: 存储的文件夹
    :return:
    '''
    #从图集URL中提取图片URL并存储图像
    #设置heander和Agent参数
    Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    headers = {"User-Agent": Agent}
    #分析URL得出，每个图集最多不超过50张，此处我们假设有100张
    for i in range(1,100):
        #第一张图片的url不需要改
        if i == 1:
            html_url = url
        #第二张开始，需要更改url
        else:
            html_url = url.split(".htm")[0] + "_" + str(i) + ".htm"
        r = requests.get(html_url,headers=headers)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content)
            #分析网页源码，可知class：ImageBody的div里面存储图片地址
            find_image_div = soup.find_all("div",attrs={'class':'ImageBody'})
            find_image_div = str(find_image_div)
            #在div中匹配图片地址
            pattern = re.compile(r'((http)?:\/\/)[^\s]+.jpg')
            #尝试用正则获取URL。有些图片中会获取不到，所以用了try。第二页第四个图集的第六张照片就匹配不到
            try:
                img_url = pattern.search(find_image_div).group(0)
            except:
                continue
            #从图片地址中获取图片并写入文件
            r = requests.get(img_url)
            image_name = forder + "/" +str(i) + ".jpg"
            if os.path.exists(image_name):
                time.sleep(1)
                print("文件已存在")
            else:
                with open(image_name,'wb') as f :
                    f.write(r.content)
                    #因为我们没有使用代理，为避免反扒，延迟1.5s
                    time.sleep(0.5)
                    print("%s已存储"%image_name)
        else:
            print("当前图集爬取完成,切换下一图集")
            break

def get_image_url(url):
    '''
    :param url: 网页URL
    :return:
    '''
    #从网页中提取图集的URL
    Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    headers = {"User-Agent":Agent}
    for i in range(10,100):
        #从URL中分析可知，不同图集页面只是尾缀不一样
        get_url = url.split(".htm")[0] + "_" + str(i) + ".htm"
        r = requests.get(get_url,headers=headers)
        #如果页面可正常访问，则提取图集地址，否则跳出循环
        if r.status_code == 200:
            soup = BeautifulSoup(r.content)
            #分析源代码可知，图集地址存储在class：TypeBigPics的a标签中
            find_a = soup.find_all("a",attrs={'class':'TypeBigPics'})
            for n,a in enumerate(find_a):
                string_a = str(a)
                #提取图集地址的正则
                pattern_url = re.compile(r'((http)?:\/\/)[^\s]+.htm')
                #提取图集名称的正则，用来创建文件夹
                pattern_forder_name = re.compile(r'<div class="ListTit">(.*)</div></a>')
                #获取图集地址及图集名称
                image_url = pattern_url.search(string_a).group(0)
                name = pattern_forder_name.search(string_a).group(1)
                print("第%s页第%s个图集开始爬取"%(i,n+1))
                print("-------------------------------------")
                #用图集名称创建文件夹
                forder = create_dir(name)
                #将图集中的图片存储在文件夹中
                get_image(image_url,forder)
                print("-------------------------------------")
        else:
            print("超出最大网页范围")
            break

if __name__ == "__main__":
    get_image_url("http://www.umei.cc/tags/shaonv.htm")
    print("爬取结束")