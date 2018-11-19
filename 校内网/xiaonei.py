from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import pymongo
from pyecharts import Bar,Map,WordCloud
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

def login(driver,url,username,pwd):

    driver.get(url)

    # 输入用户名
    input_text = WebDriverWait(driver,timeout).until(
        lambda d: d.find_element_by_id("email")
    )
    input_text.send_keys(username)
    print("输入用户名 ok")

    # 输入密码
    password = WebDriverWait(driver,timeout).until(
        lambda d: d.find_element_by_id("password")
    )
    password.send_keys(pwd)
    print("输入密码 ok")

    # 检查是否有需要输入验证码
    check_code(driver)

    # 点击登录按钮
    login_button = WebDriverWait(driver,timeout).until(
        lambda d: d.find_element_by_id("login")
    )
    login_button.click()
    print("点击登录 ok")

    # 进入个人主页
    hd_name = WebDriverWait(driver,timeout).until(
        lambda d: d.find_element_by_class_name("hd-name")
    )
    href = hd_name.get_attribute("href")
    print("找到个人主页地址 ok")
    return  href

def get_my_friends_info_list(driver,href):

    # 访问个人主页地址
    driver.get(href)
    name = driver.title
    print("访问%s的个人主页 ok"%name)

    # 进入好友列表页面
    friends_button = WebDriverWait(driver,timeout).until(
        lambda d: d.find_element_by_xpath('//*[@id="specialfriend-box"]/div[1]/div/h5/a')
    )
    friends_button.click()
    print("进入%s好友列表 ok"%name)

    # 等待3s，加载数据
    time.sleep(3)

    # 如果滚动条不是在页面最下方，证明列表需要加载，下拉至页面最下方
    len_after = 0
    len_before = 1

    # 如果下拉后的好友数量不等于下拉前好友的数量，就继续下拉页面
    while len_after != len_before:
        friends_list = WebDriverWait(driver, timeout).until(
            lambda d: d.find_elements_by_class_name("friend-detail")
        )

        # 获取下拉之前的好友数量
        len_before = len(friends_list)

        # 下拉至页面最底端
        js = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
        time.sleep(1)

        friends_list = WebDriverWait(driver, timeout).until(
            lambda d: d.find_elements_by_class_name("friend-detail")
        )

        # 获取下拉后的好友数量
        len_after = len(friends_list)
        print("%s的好友页面向下滚动到底部一次"%name)

    # 定位 friend-detail 标签
    friends_list = WebDriverWait(driver, timeout).until(
        lambda d: d.find_elements_by_class_name("friend-detail")
    )
    print("定位li标签 ok")

    # 定位 .friend-detail a 标签
    personal_home_pages = WebDriverWait(driver, timeout).until(
        lambda d:d.find_elements_by_css_selector(".friend-detail a")
    )
    print("定位a标签 ok")

    # 定位省份信息
    provinces_list = WebDriverWait(driver, timeout).until(
        lambda d: d.find_elements_by_class_name("friends-loc-info")
    )
    print("定位省份信息 ok")

    # 将定位的信息组装成字典并写入数据库
    for i in range(len(friends_list)):
        friends_info = {"data_id":friends_list[i].get_attribute("data-id"),
                        "name":friends_list[i].get_attribute("data-name"),
                        "id":friends_list[i].get_attribute("id"),
                        "personal_home_page":personal_home_pages[i].get_attribute("href"),
                        "province":provinces_list[i].get_attribute("title"),
                        "status":0,
                        "from":name,
                        }
        print(friends_info["province"], friends_info["name"])

        #将获取到的数据写入数据库
        write_to_mongo(friends_info,i,name)

    driver.quit()

def get_friend_friends_page_source(f,page_source_list):
    """
    由于缓存机制，先访问一遍个人主页，再用同一浏览器访问好友主页
    """
    option = webdriver.ChromeOptions()
    option.add_argument("headless")

    #下面这行注释掉就是无头浏览器，如果不注释，在运行时会打开浏览器
    # driver = webdriver.Chrome()

    driver = webdriver.Chrome(chrome_options=option)
    driver.get("http://www.renren.com")

    # 输入用户名
    input_text = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_id("email")
    )
    input_text.send_keys("你的账号")
    print("输入用户名 ok")

    # 输入密码
    password = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_id("password")
    )
    password.send_keys("你的密码")
    print("输入密码 ok")

    # 检查是否需要输入验证码
    check_code(driver)

    # 点击登录
    login_button = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_id("login")
    )
    login_button.click()
    print("点击登录 ok")

    # 获取好友个人主页地址及好友姓名
    href = f["personal_home_page"]
    name = f["name"]

    # 访问好友个人主页
    driver.get(href)
    print("访问%s的个人主页 ok" % name)

    # 进入好友的好友列表页面
    friends_button = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_xpath('//*[@id="specialfriend-box"]/div[1]/div/h5/a')
    )
    friends_button.click()
    print("进入%s好友列表 ok" % name)

    try:
        driver.find_element_by_id("friends_list_con")
    except Exception as e :
        print("由于对方设置隐私保护，您没有权限查看对方好友！")
        return

    # 同理，下拉页面至最底端
    len_after = 0
    len_before = 1

    while len_after != len_before:

        friends_list = WebDriverWait(driver, timeout).until(
            lambda d: d.find_elements_by_class_name("recommend-detail")
        )

        len_before = len(friends_list)

        js = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
        time.sleep(1)

        friends_list = WebDriverWait(driver, timeout).until(
            lambda d: d.find_elements_by_class_name("recommend-detail")
        )
        len_after = len(friends_list)
        print("%s的好友页面向下滚动到底部一次"%name)

    page_source_list.append(driver.page_source)
    print("%s的好友页面page_source已经添加到列表中"%name)

    # 更改已经爬取过的好友的状态，方便以后筛选
    f["status"] = 1

    # 将状态写入数据库
    change_friend_status(f)

    #关闭浏览器
    driver.close()

def check_friend_name(data_id):
    """
    如果需要过滤好友信息，使用此方法
    """

    # 查询数据库
    result = []
    curr = pymongo.MongoClient()
    database = curr["renren"]
    coll = database['friends']
    data = coll.find({"data_id": data_id})

    for d in data:
        result.append(d)
    curr.close()

    if result:
        print("好友重复")
        return True
    else:
        print("好友不重复")
        return False

def change_friend_status(f):

    #读取数据库并更新状态
    curr = pymongo.MongoClient()
    database = curr["renren"]
    coll = database['friends']
    coll.update_one({"name":f["name"]},{'$set':f})
    print("更新%s的状态成功"%(f["name"]))
    curr.close()

def write_to_mongo(friends_info,i,name):

    # 将数据写入数据库
    curr = pymongo.MongoClient()
    database = curr["renren"]
    coll = database['friends']
    coll.insert(friends_info)
    print("%s的第%s个好友写入数据库成功"%(name,i+1))
    curr.close()

def search_mongo():

    # 查询数据库中还未爬取过的信息，status = 0 未爬取 ； status = 1 爬取过
    curr = pymongo.MongoClient()
    database = curr["renren"]
    coll = database['friends']
    friends_list_to_crawl = coll.find({"status":0})
    curr.close()
    return friends_list_to_crawl

def check_code(driver):

    # 检查验证码输入框（验证码这个控件即使不需要输入也存在。。。被骗了，还没想好如何自动判断，目前只能人工判断）
    try:
        icode = driver.find_element_by_xpath('//*[@id="icode"]')
        print("找到了验证码")
    except Exception as e:
        icode = None
        print("未找到验证码")

    """
    如果遇到访问次数过多，需要输入验证码的情况，将下面这段注释打开
    """
    # if icode != None:
    #     image_url = driver.find_element_by_xpath('//*[@id="verifyPic_login"]').get_attribute("src")
    #     r = requests.get(image_url)
    #     with open("icode.jpg","wb") as f:
    #         f.write(r.content)
    #
    #     icode_input = input("请输入验证码：")
    #     icode.send_keys(icode_input)

def fenxi():
    # 读取数据库中的数据
    curr = pymongo.MongoClient()
    database = curr["renren"]
    coll = database['friends']
    friends_list_all_find = coll.find({})
    friends_list_all = []
    for f in friends_list_all_find:
        friends_list_all.append(f)
    curr.close()

    # 统计省份信息
    result = {}
    for f in friends_list_all:
        if f["province"] not in result.keys():
            result[f["province"]] = 1
        else:
            result[f["province"]] += 1

    # 对统计数据进行过滤，去除没有省份的数据和小于100的数据
    result_gt100 = {}
    for k,v in result.items():
        if v >= 100:
            if k.strip():
                result_gt100[k] = v

    # 对数据按照省份值进行排序
    result_gt100_sorted = sorted(result_gt100.items(), key=lambda x: x[1], reverse=True)

    # 统计出key列表和value列表，下面生成统计图使用
    key = []
    value = []
    for k in result_gt100_sorted:
        key.append(k[0])
        value.append(k[1])
    # 柱形图
    bar = Bar("柱状图",width=2000,height=1000)
    bar.add("",key,value,is_label_show=True)
    bar.render(path="柱状图.html")

    # 全国地图
    map = Map("全国地图示例", width=2000, height=1000)
    map.add("", key, value, maptype='china',is_visualmap=True, visual_text_color="#000",is_map_symbol_show = False,
            visual_range=[0, 1000])
    map.render(path="地图.html")

    # 词云图
    wordcloud = WordCloud(width=2000, height=1000)
    wordcloud.add("", key, value, word_size_range=[50, 250])
    wordcloud.render(path="词云.html")

def get_friend_friends_list(page_source):
    soup = BeautifulSoup(page_source,"lxml")

    # 定位 recommend-detail 标签
    # friends_list = WebDriverWait(driver, timeout).until(
    #     lambda d: d.find_elements_by_class_name("recommend-detail")
    # )
    friends_list = soup.find_all(class_ ="recommend-detail")
    print("定位li标签 ok", len(friends_list))

    # 定位 userhead 标签
    # personal_home_pages = WebDriverWait(driver, timeout).until(
    #     lambda d: d.find_elements_by_class_name("userhead")
    # )
    personal_home_pages = soup.find_all(class_ ="userhead")
    print("定位a标签 ok", len(personal_home_pages))

    # 定位省份信息
    # provinces_list = WebDriverWait(driver, timeout).until(
    #     lambda d: d.find_elements_by_class_name('friends-loc-info ')
    # )
    provinces_list = soup.find_all(class_ = 'friends-loc-info ')
    print("定位省份信息 ok", len(provinces_list))

    name = soup.find(class_ = "fd-nav-item").get_text().strip()
    print("%s一共有%s个好友" % (name, len(friends_list)))

    for i in range(len(friends_list)):
        friends_info = {"data_id": friends_list[i].attrs["data-id"],
                        "name": friends_list[i].attrs["data-name"],
                        "id": friends_list[i].attrs["data-id"],
                        "personal_home_page": personal_home_pages[i].attrs["href"],
                        "province": provinces_list[i].attrs["data"],
                        "status": 0,
                        "from": name,
                        }
        print(friends_info["province"], friends_info["name"])

        # 因为好友间的好友会有重复，如果想要去重就打开下面的注释
        if not check_friend_name(friends_info["data_id"]):
            write_to_mongo(friends_info, i, name)

if __name__ == "__main__":

    # 设置基础参数
    timeout = 10
    username = "你的账号"
    pwd = "你的密码"
    option = webdriver.ChromeOptions()
    option.add_argument("headless")

    # 有头浏览器
    # driver = webdriver.Chrome()

    #无头浏览器
    driver = webdriver.Chrome(chrome_options=option)
    href = login(driver,"http://www.renren.com",username,pwd)

    #访问个人主页，获取自己的好友列表
    get_my_friends_info_list(driver,href)

    n = 0
    while n < 6:
        print("-"*100)
        print("开始第%s轮爬取"%(n+1))
        print("-" * 100)
        friends_list_to_crawl = []
        for f in search_mongo():
            friends_list_to_crawl.append(f)
        print("列表读取完成")

        # 爬取好友的好友信息
        print("开始抓取好友信息")

        page_source_list = []
        ex_get_page_source = ThreadPoolExecutor(max_workers=3)
        for f in friends_list_to_crawl:
            ex_get_page_source.submit(get_friend_friends_page_source,f,page_source_list)
        ex_get_page_source.shutdown(wait=True)

        ex_get_friends_list = ThreadPoolExecutor(max_workers=20)
        for p in page_source_list:
            ex_get_friends_list.submit(get_friend_friends_list,p)
        ex_get_friends_list.shutdown(wait = True)

        n += 1

    """上面的执行完成后，下面的代码进行结果分析"""
    fenxi()