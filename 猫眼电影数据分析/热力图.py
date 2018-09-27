import pandas as pd
from pyecharts import Geo

tomato_com = pd.read_excel('西红柿.xlsx')

grouped=tomato_com.groupby(['cityName'])

grouped_pct=grouped['score'] #tip_pct列

city_com = grouped_pct.agg(['mean','count'])

city_com.reset_index(inplace=True)

city_com['mean'] = round(city_com['mean'],2)

data_all=[(city_com['cityName'][i],city_com['mean'][i]) for i in range(0,city_com.shape[0])]

geo = Geo("《西虹市首富》全国热力图", title_color="#fff",
          title_pos="center", width=1200,
          height=600, background_color='#404a59')

for data in data_all:
    attr, value = geo.cast([data])
    try:
        geo.add("", attr, value, visual_range=[4, 5], maptype='china', visual_text_color="#fff",
                symbol_size=10, is_visualmap=True)
    except:
        pass
