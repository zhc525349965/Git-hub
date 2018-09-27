from  pyecharts import WordCloud
import csv
import jieba

def worldcloud():
    #读取csv中的title信息，将所有title信息放入一个字符串中
    data_string = ""
    with open("jd.csv","r") as csvfile :
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_string += row['title']
    #使用jieba分词，将上一步获取的字符串分词，并根据分词结果进行统计
    seg_count = {}
    seg_list = jieba.cut(data_string, cut_all=False)
    for seg in seg_list:
        if seg not in seg_count.keys():
            seg_count[seg] = 1
        else:
            seg_count[seg] += 1

    #只保留出现次数在100次以上的词汇（可根据爬取结果更改）
    seg_count_bigthan100 = seg_count.copy()
    for k,v in seg_count.items():
        if v < 100:
            seg_count_bigthan100.pop(k)

    #去除无用的词汇
    rubbish_list = [' ',"（","）","【","】",'+','-','~','/','、','，','。','！']
    for i in rubbish_list:
        try:
            seg_count_bigthan100.pop(i)
        except:
            pass

    #使用WordCloud生成词云
    word = []
    count = []
    wordcloud = WordCloud(width=1300, height=620)
    for k,v in seg_count_bigthan100.items():
        word.append(k)
        count.append(v)
    wordcloud.add("词云图", word, count, word_size_range=[20, 100],shape="diamond")
    wordcloud.render()