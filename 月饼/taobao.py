import requests
import re
import threading
import os
from pyecharts import Bar
from concurrent.futures import ThreadPoolExecutor

def get_product_id_list(num,all_product_list):
    base_url = "https://s.taobao.com/search"
    params = {
        "q":"月饼散装",
        "s":num*44,
    }

    r = requests.get(base_url,params=params,headers=headers)

    nids=re.findall(pattern='"nid":"(.*?)"',string=r.text)

    for nid in nids:
        if nid not in all_product_list:
            all_product_list.append(nid)

    print("第%s页product-id提取完成"%num)
    return all_product_list

def get_product_comments(num,):
    print("开始爬取第%s条的商品评论"%num)
    with open("all_product_list.txt","r") as f :
        all_product_list = eval(f.read())
    product_id = all_product_list[num]
    base_url = "https://rate.taobao.com/feedRateList.htm"
    currentPageNum = 1
    product = {}

    while True:
        params = {
            "auctionNumId":product_id,
            "currentPageNum":currentPageNum
        }
        r = requests.get(base_url,params=params,headers=headers)
        try:
            data = eval(r.text.strip("(").strip(")").replace("true","True").replace("false","False").replace("null","None"))
            total = data["total"]
        except:
            total = 0
        if total != 0:
            comments = data["comments"]
            for comment in comments:
                auction = comment["auction"]
                sku = auction["sku"]
                if sku in product.keys():
                    product[sku] += 1
                else:
                    product[sku] = 1
        else:
            break
        print("第%s条商品的第%s页评论爬取完成"%(num,currentPageNum))
        currentPageNum += 1
    print("第%s条商品的评论爬取完成" % num)

    if not os.path.exists("product_type.txt"):
        with open("product_type.txt","w") as f :
            f.close()
    lock.acquire()
    try:
        print("开始写入第%s条商品的评论数据" % num)
        with open("product_type.txt","r+") as f :
            print("-"*200)
            content = f.read()
            if not content:
                product_type = {}
            else:
                product_type = eval(content)

            for k,v in product.items():
                if k in product_type.keys():
                    product_type[k] += v
                else:
                    product_type[k] = v
            f.seek(0)
            f.truncate()
            f.write(str(product_type))
            print("-" * 200)
    finally:
        lock.release()
    print("第%s条商品的评论数据写入完成" % num)

def word_cloud():
    with open("product_type.txt", "r")as f:
        content = f.read()
        product_type = eval(content)
    k = product_type.keys()
    v = product_type.values()
    k = list(k)
    v = list(v)
    bar = Bar("柱形图")
    bar.add("月饼销售记录", k, v, xaxis_rotate=90, )
    bar.render()


if __name__ == "__main__":
    headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "cookie":"miid=843893066219719277; t=88784b17959ea7f8c82cf0676aadb4a3; cna=nTydE8WIfRgCAd3YM6qXapga; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; tracknick=zhc525349965; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; enc=gkqJ9e%2BbXX57uOuy1%2Fiyq99tGNpQQZ9vAJ7f44hIXbTcesTybOz%2BkoWQ4sFxciQAAYnwyPqEcl1nucna2fzk2g%3D%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; UM_distinctid=165d1d640293e8-0003adcc256058-9393265-384000-165d1d6402b426; v=0; cookie2=368691db898a9da80fc9d799d25f9bc4; _tb_token_=e6f68634359e5; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=E7AD1CD8AAC658AAD982483B5ACB2E18; isg=BC8v8yr6qAGllay-_Xu_Iqm1vkP5fIKQ_It59UG8yx6lkE-SSaQTRi1CFsAL6Ftu",
    }
    all_product_list = []
    product_type = {}
    lock = threading.Lock()
    for num in range(101):
        all_product_list = get_product_id_list(num,all_product_list)

    with open("all_product_list.txt","w") as f :
        f.write(str(all_product_list))

    with open("all_product_list.txt","r") as f :
        all_product_list = eval(f.read())

    len_all_product_list = len(all_product_list)
    print("一共提取%s条商品id"%len_all_product_list)

    ex = ThreadPoolExecutor(max_workers=500)
    res_iter = ex.map(get_product_comments, range(len_all_product_list))