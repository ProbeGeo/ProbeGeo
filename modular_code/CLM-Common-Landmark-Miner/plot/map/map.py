from pyecharts.charts import Geo
from pyecharts import options
from pyecharts.globals import GeoType
import os
import pandas as pd
import json

results = pd.read_csv(os.path.join('..', 'data', 'result.csv'))
types = set(results['type'].tolist())

g = Geo(init_opts=options.InitOpts(width='1200px', height='700px')).add_schema(maptype="world")
con_ips = []
con_latitudes = []
con_longitudes = []
uncon_ips = []
uncon_latitudes = []
uncon_longitudes = []
for type_ in types:
    ips = results[results['type'] == type_]['ip'].tolist()
    latitudes = results[results['type'] == type_]['latitude'].tolist()
    longitudes = results[results['type'] == type_]['longitude'].tolist()
    if type_ == 'lg' or type_ == 'pf':
        con_ips.extend(ips)
        con_latitudes.extend(latitudes)
        con_longitudes.extend(longitudes)
    else:
        uncon_ips.extend(ips)
        uncon_latitudes.extend(latitudes)
        uncon_longitudes.extend(longitudes)
for ip, longitude, latitude in zip(con_ips, con_longitudes, con_latitudes):
    g.add_coordinate(ip, longitude, latitude)
con_data_pair = [(ip, 1) for ip in con_ips]
g.add('probe landmarks', con_data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=5, color='blue')
for ip, longitude, latitude in zip(uncon_ips, uncon_longitudes, uncon_latitudes):
    g.add_coordinate(ip, longitude, latitude)
uncon_data_pair = [(ip, 1) for ip in uncon_ips]
g.add('common landmarks', uncon_data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=2, color='red')
g.set_series_opts(label_opts=options.LabelOpts(is_show=False))
g.set_global_opts(legend_opts=options.LegendOpts(is_show=True, textstyle_opts=options.TextStyleOpts(font_size=30, font_weight='bold'), pos_top='8%'))
g.render(os.path.join('map.html'))

# 
# for ip, longitude, latitude in zip(ips, longitudes, latitudes):
#     g.add_coordinate(ip, longitude, latitude)
# for windy_ip, windy_longitude, windy_latitude in zip(windy_ips, windy_longitudes, windy_latitudes):
#     g.add_coordinate(windy_ip, windy_longitude, windy_latitude)

# data_pair = [(ip, 1) for ip in ips]
# windy_data_pair = [(windy_ip, 1) for windy_ip in windy_ips]


# g.add('windy', windy_data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=2, color='blue')
# g.add('pictimo', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=2, color='red')

# g.set_series_opts(label_opts=options.LabelOpts(is_show=False))

# g.set_global_opts(title_opts=options.TitleOpts(title="test"))
# g.render("map2.html")