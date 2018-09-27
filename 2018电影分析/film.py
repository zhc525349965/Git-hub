import re
import requests
import json
import jieba
import jieba.analyse

#获取目标电影
while(1):
    line=input('请输入电影在猫眼网中的链接：')
    #line='http://maoyan.com/films/1200486'
    if re.search('maoyan.com/films',line) is None:
        print('输入有误！请重新输入！')
    else:
        line=re.sub(' ','',line)
        filmid=re.search('films/(\d*)$',line)
        filmid=filmid.group(1)
        print('成功获取电影ID：',filmid)
        break

#模拟PC端获取电影名称
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Host':'maoyan.com'
        }
title= requests.get ( line , headers = headers )
if title.status_code != 200 :
    print('解析错误！请稍后重试！')
    print(title.status_code)
    exit(0)
title=re.search('content="(.*?),在线观看',title.text)
title=title.group(1)

#模拟手机端获取最新评论信息
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Host':'m.maoyan.com'
        }
rate=[]
city=[]
comment = []

#开始获取尽可能多的评论信息
for i in range(1,1001):
    data= requests.get ( 'http://m.maoyan.com/mmdb/comments/movie/'+str(filmid)+'.json?_v_=yes&offset='+str(i), headers = headers )
    if data.status_code != 200 :
        print('解析错误！请稍后重试！')
        print(data.status_code)
    print('正在爬取第',i,'页数据！')
    data=data.text
    try:
        data = json.loads(data)['cmts']
    except KeyError:
        break
    for more in data:
        comment.append(more['content'])
        rate.append(more['score'])
        city.append(more['cityName'])

#统计获取的评论数量
n=comment.__len__()

#评论分词
deal=str(comment)
cut_text=" ".join(jieba.cut(deal, cut_all=False))
cut_text=re.sub('公寓','',cut_text)
cut_text=re.sub('爱情','',cut_text)
topword=jieba.analyse.extract_tags(deal,35)
value = [cut_text.count(a) for a in topword]

#准备生成页面
from pyecharts import  Page
page = Page()


#获得评分水球
from pyecharts import Liquid

liquid = Liquid(title +  "---猫眼最新"+str(n)+'位用户预测评分', title_color="#fff",
          title_pos="center", width=1800,
          height=700)
nsum=0
for i in range(0,len(rate)):
    nsum+=i
lrate=nsum/len(rate)
liquid.add("评分值", [lrate/100])
page.add_chart(liquid)
print(nsum)
print(lrate)
print(len(rate))
print(rate)
#生成观众评分图
from pyecharts import Pie
attr = ["五星", "四星", "三星", "两星", "一星"]
v1 = [rate.count(5)+rate.count(4.5), rate.count(4)+rate.count(3.5),rate.count(3)+rate.count(2.5),rate.count(2)+rate.count(1.5),rate.count(1)+rate.count(0.5)]
rate = Pie(title+"---猫眼用户评分图",title_pos='center',width=1800, height=620)
rate.add("", attr, v1, radius=[40, 75], label_text_color=None,
        is_label_show=True, legend_orient='vertical',
        legend_pos='left')
page.add_chart(rate)


#生成评论词云图
from pyecharts import WordCloud
wordcloud = WordCloud(title +  "---猫眼最新"+str(n)+'条评论关键词云图',width=1800, height=620, title_pos="center")
wordcloud.add("", topword, value, word_size_range=[20, 100])
#shape -> list
#词云图轮廓，有'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star'可选
# wordcloud.render(path='wordcloud.html')
page.add_chart(wordcloud)

#生成评论词频图
from  pyecharts import  Bar
bar = Bar(title +  "---猫眼最新"+str(n)+'条评论关键词', title_color="#fff",
          title_pos="center", width=1800,
          height=700)
bar.add("", topword, value, is_visualmap=True, visual_range=[0, 5000], visual_text_color='#fff',
        mark_point=["average"], mark_line=["average"],
        is_piecewise=True, visual_split_number=10, is_more_utils=True, )
page.add_chart(bar)

#生成观众地图分布
from pyecharts import Geo
cityy=set(city)
citydata={a:city.count(a) for a in cityy}
geo = Geo(title +  "---猫眼最新"+str(n)+'条评论用户分布图', title_color="#fff",
          title_pos="center", width=1300,
          height=620, background_color='#404a59')

#排除数据库中未收录的城市
while(1):
    try:
        attr, value = geo.cast(citydata)
        geo.add("", attr, value, visual_range=[0, 200], maptype='china',visual_text_color="#fff",
                is_piecewise=True,visual_split_number=10,symbol_size=10, is_visualmap=True)
        #geo.render(path='geo.html')
        page.add_chart(bar)
        page.add_chart(geo)
        break
    except ValueError as Argument:
        Argument=str(Argument)
        Argument=re.search('No coordinate is specified for (.*)',Argument)
        Argument=Argument.group(1)
        citydata.pop(Argument)
#生成页面文件
page.render()