import telnetlib
import requests
from bs4 import BeautifulSoup
import time
import pymongo

def get_ip(exist_ip):
    url = 'https://www.kuaidaili.com/free/inha/'
    result = []
    page = 1
    localTime = time.localtime(time.time())
    today = time.strftime("%Y-%m-%d", localTime)
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }

    while True :
        target_url = url + str(page)

        re = requests.get(target_url,headers = headers)
        soup = BeautifulSoup(re.text,'lxml')
        ip_lists = soup.findAll(name='tr')[1:]

        for ips_info in ip_lists:
            item = {}
            ip_info = ips_info.findAll(name = 'td')
            item['ip'] = ip_info[0].text
            item['port'] = ip_info[1].text
            item['niming'] = ip_info[2].text
            item['type'] = ip_info[3].text
            item['location'] = ip_info[4].text
            item['speed'] = ip_info[5].text
            item['verify_time'] = ip_info[6].text

            if item['verify_time'].split(' ')[0] != today:
                return result

            if item['ip'] not in exist_ip:

                if check_ip(item['ip'],item['port']):

                    result.append(item)
                    save_ip(item)
            else:
                print('%s已经存在'%item['ip'])

        page += 1

        time.sleep(5)

def check_ip(ip,port):
    try:
        telnetlib.Telnet(ip,port=port,timeout=10)
    except:
        print("%s:%s Fail"%(ip,port))
        return False
    else:
        print("%s:%s OK"%(ip,port))
        return True

def save_ip(item):
    conn = pymongo.MongoClient()
    db = conn['ip-pools']
    collection = db['ip']
    collection.insert_one(item)
    print('%s:%s添加书入库成功'%(item['ip'],item['port']))
    conn.close()

def exist_ip():
    exist_ip = []
    conn = pymongo.MongoClient()
    db = conn['ip-pools']
    collection = db['ip']
    for ip in collection.find({}):
        exist_ip.append(ip['ip'])
    conn.close()
    return exist_ip

def check_exist_ip():
    conn = pymongo.MongoClient()
    db = conn['ip-pools']
    collection = db['ip']
    n = 0
    for ip in collection.find({}):
        try:
            telnetlib.Telnet(ip['ip'], port=ip['port'], timeout=10)
        except:
            collection.delete_one({'ip': ip['ip']})
            print('%s未通过检测，已删除' % ip['ip'])
        else:
            print('%s通过检测，保留' % ip['ip'])
            n += 1
    print("还剩下%s个ip可用" % n)

if __name__ == "__main__":
    check_exist_ip()
    exist_ip = exist_ip()
    get_ip(exist_ip)