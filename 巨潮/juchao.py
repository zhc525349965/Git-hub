import requests
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
import os

base_url = "http://www.cninfo.com.cn/cninfo-new/fulltextSearch/full"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}

def get_return_data(pageNum,searchkey="社会责任"):

    params = {
        "searchkey":searchkey,
        "sdate":"",
        "edate":"",
        "isfulltext":"false",
        "sortName":"nothing",
        "sortType":"desc",
        "pageNum":pageNum,
    }

    r = requests.get(base_url,params=params,headers=headers)
    if r.status_code == 200:
        content = r.json()
        return  content
    else:
        return None

def get_announcement_info(content):

    announcements = content["announcements"]
    announcement_base_url = "http://www.cninfo.com.cn/cninfo-new/disclosure/fulltext/bulletin_detail/true/"

    for announcement in announcements:
        announcement_detail_url = (announcement_base_url+announcement["announcementId"])

        r = requests.get(announcement_detail_url)
        soup = BeautifulSoup(r.content,"lxml")

        title = soup.select("body > div.middle > div.main > div.bd-top > h2")[0]
        title = (title.get_text().strip("\r\n\t\t\t\t\t").split("\r\n\t\t\t\t\t")[-1])

        document_url = soup.select("body > div > div.main > div.bd-rt > div.bd-download > div > a")[0]
        document_url = "http://www.cninfo.com.cn/" + document_url["href"]

        modify_time = document_url.split("announceTime=")[1]

        yield {
            "title":title,
            "document_url":document_url,
            "modify_time":modify_time,
        }

def save_pdf(announcement,pageNum):
    title = announcement['title']
    modify_time = announcement['modify_time']
    file_name = "pdf"+ os.path.sep + title + "-" + modify_time + ".pdf"
    document_url = announcement['document_url']

    with open(file_name,"wb") as f :
        f.write(requests.get(document_url).content)
        print("第%s页，%s保存完成"%(pageNum,title))

def main(pageNum):
    return_content = get_return_data(pageNum)
    if return_content != None:
        announcement_info = get_announcement_info(return_content)
        for announcement in announcement_info:
            save_pdf(announcement,pageNum)

if __name__ == "__main__":
    pool = Pool()
    start_page = 0
    end_page = 10
    groups = ([x for x in range(start_page, end_page + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()