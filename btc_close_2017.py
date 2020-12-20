from os import write
import pygal
import math
from itertools import groupby
import json
#####################################
filename = 'btc_close_2017.json'
with open(filename) as f:
    btc_data = json.load(f)

dates = []
months = []
weeks = []
weekdays = []
close = []  #变量和字典键不冲突??
x_date_y_close = []
for btc_dict in btc_data:
    date = btc_dict['date']
    dates.append(date)
    months.append(int(btc_dict['month']))
    weeks.append(int(btc_dict['week']))
    weekdays.append(btc_dict['weekday'])
    close0 =int(float(btc_dict['close']))
    close.append(close0)
################################
print('#'*46)
print('##  数据日期区间= ',dates[0],'~~',dates[-1],'##')
print('#'*46)
#########################
star_day = '2017-03-02'
end_day  = '2017-10-01'
#########################
print('##  视图显示日期= ',star_day,'~~',end_day,'##')
print('#'*46)
idx_star = dates.index(star_day)
idx_end = dates.index(end_day)+1
dates_s2e = dates[idx_star:idx_end]
################################

line_chart = pygal.Line(x_label_rotation=20,show_minor_x_labels=False)
line_chart_title = '收盘价(￥)'
line_chart.x_labels = dates_s2e
N = 21      #x轴坐标每21天显示一次
line_chart.x_labels_major = dates_s2e[::N]
line_chart.add('收盘价', close[idx_star:idx_end])
line_chart.render_to_file('收盘价折线图(￥).svg')
#############################

line_chart_log = pygal.Line(x_label_rotation=20,show_minor_x_labels=False)
line_chart_log.title = '收盘价对数变换(￥)'
line_chart_log.x_labels = dates_s2e
M=21
line_chart_log.x_labels_major = dates_s2e[::M]
close_log = [math.log10(_) for _ in close[idx_star:idx_end]]
line_chart_log.add('log收盘价',close_log)
line_chart_log.render_to_file('收盘价对数变换折线图(￥).svg')
line_chart_log

""""
时间段内均值函数定义
"""

#from itertolls import groupby
#创建均值绘图函数
def draw_line(x_data,y_data,title,y_legend):
    xy_map = []    ### x日期/时间，y收盘价(均值)
    for key_x,x_and_y in groupby(sorted(zip(x_data,y_data)),key=lambda _: _[0]):
        ### zip将x_data,y_data两个列表中的数据一对一打包为元组再组成列表；
        ### sorted 将组成的列表元素进行排序成新的列表;
        ### itertools.groupby 按key对列表的元素进行分组聚合 ;
        ### lambda _: 匿名函数，_是临时变量即为列表元素(x_data,y_data),_[0]为x_data；
        ### x,y ==> x=key=x_data,y=[list(x_data,y_data)....]
        y_g_list = [v for _, v in x_and_y]  ## 遍历key,[list(x_data,y_data)]进行循环
        ###y_g_list为key分组对应的y_data值列表;  _,v == (_,v)对应[list(x_data,y_data)]
        key_and_values = [key_x,sum(y_g_list)/len(y_g_list)]
        ### y_g_list是为获取数值列表，才可以进行sum运算。
        xy_map.append(key_and_values)
    x_unique,y_mean = [*zip(*xy_map)]
    ### xy_map ==>> [list(x,y)] ; zip(*xy_map) ==>> [list(x),list(y)]
    ### [*zip(*xy_map)] ==>> list(x),list(y)---不是list了
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = x_unique
    line_chart.add(y_legend,y_mean)
    line_chart.render_to_file(title+'.svg')
    return line_chart

###########

line_chart_month =draw_line(months[idx_star:idx_end],close[idx_star:idx_end],'收盘价月的日均值(￥)','月-日均值')
line_chart_month  ###这一行什么用？？

####################

line_chart_week = draw_line(weeks[idx_star:idx_end],close[idx_star:idx_end],'收盘价周-日均值(￥)','周-日均值')
line_chart_week

#####################
#weekday转int
wd=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekdays_int = [wd.index(w)+1 for w in weekdays[idx_star:idx_end]]
line_chart_weekday = draw_line(weekdays_int,close[idx_star:idx_end],'收盘价星期-日均值(￥)','星期-日均值')
line_chart_weekday.x_labels = ['周一','周二','周三','周四','周五','周六','周日']
line_chart_weekday.render_to_file('收盘价星期-日均值(￥).svg')
####################

with open('BTC收盘价看板Dashboard.html','w',encoding='utf8') as html_file:
    html_file.write('<html><head><title>BTC收盘价Dashboard</title><meta charset="utf-8"></head><body>\n')
    for svg in [
            '收盘价折线图(￥).svg','收盘价对数变换折线图(￥).svg',
            '收盘价月的日均值(￥).svg','收盘价周-日均值(￥).svg',
            '收盘价星期-日均值(￥).svg'  ]:
        html_file.write('   <object type="image/svg+xml" data="{0}" height=550></object>\n'.format(svg))
    html_file.write('</body></html>')
