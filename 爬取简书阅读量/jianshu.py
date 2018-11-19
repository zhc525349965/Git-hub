import requests
import time
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    # 'cookie':'read_mode=day; default_font=font2; locale=zh-CN; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1541317558,1542022859; _m7e_session=37c42acbe9cb292b69b2a15a8f119a48; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2214931526%22%2C%22%24device_id%22%3A%22166ddaf803129e-09b472dafbaafb-1e386652-1296000-166ddaf8032dd5%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22166ddaf803129e-09b472dafbaafb-1e386652-1296000-166ddaf8032dd5%22%7D; __yadk_uid=3nYvMcjT94lZaDG6rrNdqxvm3K0GFaCu; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1542032887',
}
base_url = 'https://www.jianshu.com/u/130f76596b02?order_by=shared_at&page='


def get_articles_url():
    target_urls = []
    for n in range(1,2):
        url = base_url + str(n)
        html = requests.get(url,headers=headers)
        soup = BeautifulSoup(html.text,'lxml')
        # print(soup)
        hrefs = soup.find_all(class_ = 'title')
        for href in hrefs:
            sub_url = href.get('href')
            if sub_url != None:
                target_urls.append('https://www.jianshu.com' + str(href.get('href')))
        print('第%s页链接爬去完成')
        time.sleep(5)
    return target_urls

def get_views_count(target_urls):
    for url in target_urls:
        html = requests.get(url,headers=headers)
        soup = BeautifulSoup(html.content.decode('utf-8'),'lxml')
        title = soup.find(class_ = 'title').text
        print(title)
        views_count = eval(soup.find('script',attrs={'data-name':'page-data'}).text.replace('false','False').replace('null','None').replace('true','True'))['note']['views_count']
        print(views_count)
        print("#"*200)


if __name__ == "__main__":
    target_urls = get_articles_url()
    get_views_count(target_urls)
