from pyecharts import Bar,Pie,WordCloud
from pyecharts.engine import create_default_environment

type_list1 = ["豆沙","莲蓉","椰蓉","混合","五仁","枣泥","蛋黄","青红丝","桂花","梅干","玫瑰","冰糖","白果","肉松",
             "黑芝麻","火腿","礼盒","原味","乳酸菌","牛肉","榴莲","蓝莓","芒果","抹茶"]
type_list2 = ["京式","广式","滇式","潮式","苏式","台式","港式","徽式","衢式",
              "秦式","晋式","日式"]
type_list3 = ["甜","咸","麻辣"]
type_list4 = ['浆','混糖','酥皮','奶油','冰皮']
new_content = {"其他":0}

with open("product_type1.txt","r")as f :
    content = f.read()
    product_type = eval(content)

for k,v in product_type.items():
    flag = False
    for type in type_list1:
        if type in k:
            flag = True
            if type not in new_content.keys():
                new_content[type] = v
            else:
                new_content[type] += v
    if flag == False:
        new_content["其他"] += v

k = new_content.keys()
v = new_content.values()
k = list(k)
v = list(v)
bar = Bar("柱形图")
bar.add("月饼销售记录", k, v, xaxis_rotate=90,)

pie = Pie("饼图-圆环图示例", title_pos='center')
pie.add(
    "",
    k,
    v,
    radius=[40, 75],
    label_text_color=None,
    is_label_show=True,
    legend_orient="vertical",
    legend_pos="left",
)

wordcloud = WordCloud(width=1300, height=620)
wordcloud.add("词云", k, v, word_size_range=[20, 100])
wordcloud.render()

env = create_default_environment("html")

env.render_chart_to_file(bar, path='bar.html')
env.render_chart_to_file(pie, path='pie.html')
env.render_chart_to_file(wordcloud, path='wordcloud.html')



