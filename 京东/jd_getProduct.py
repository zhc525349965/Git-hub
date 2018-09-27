import requests
from bs4 import BeautifulSoup
import csv

def get_item(keyword,file):
    url = "https://search.jd.com/Search"
    params = {
        "keyword":keyword,
        "enc":"utf-8",
        "s":50,
    }
    #编号
    num = 1
    #产品列表，列表内容是每个product_info的字典
    product_list = []

    for i in range(1,200,2):
        params['page'] = i

        r = requests.get(url,params=params,)
        r_content = (r.content.decode("utf-8"))
        content = BeautifulSoup(r_content,'lxml')
        product = content.select(".gl-item")
        for p in product:
            product_info = {}
            product_info['number'] = num
            num += 1
            try:
                #价格
                product_info["price"] = p.select(".p-price i")[0].get_text()
                #商品名称
                product_info["title"] = p.select('.p-name-type-2 a')[0].attrs['title'].strip(" ")
                #商品链接
                product_info['product_detail_link'] = p.select('.p-img a')[0].attrs['href'].strip('/')
                #图片链接
                product_info['img_link'] = p.select('.p-img a img')[0].attrs['source-data-lazy-img'].strip('/')
                #评价数量
                product_info["评价数量"] = p.select('.p-commit a')[0].get_text()
                #商家信息
                shop = p.select(".p-shop a")
                if len(shop) == 0 :
                    shop_name = ""
                    shop_link = ""
                else:
                    #商铺名称
                    shop_name = shop[0].get_text()
                    #商铺链接
                    shop_link = shop[0].attrs['href']
                product_info['shop_name'] = shop_name
                product_info['shop_link'] = shop_link
            except:
                print("没有找到指定内容")
            #将product_info传入list
            product_list.append(product_info)

        print("第%s爬取完成"%i)
    #调用存储方法
    save_info(product_list,file)

def save_info(product_list,file):
    fieldnames = ['number','price','title','product_detail_link','img_link',"评价数量",'shop_name','shop_link']
    with open(file,'a',newline="") as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for product_info in product_list:
            #写入时需要注意，有些商品名称包含“✅”或“❤”特殊字符，是无法写入的，要做处理
            try:
                writer.writerow(product_info)
            except:
                print(str(product_info) + "写入错误")

def jd():
    keyword = input("输入想要搜索的内容：")
    file = "jd.csv"
    get_item(keyword,file)

