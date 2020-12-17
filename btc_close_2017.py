import json
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
    d_c=(date,close0+10000)
    x_date_y_close.append(d_c)

#########################
import pygal

line_chart = pygal.Line(x_label_rotation=20,show_minor_x_labels=False)
line_chart_title = '收盘价(￥)'
line_chart.x_labels = dates
N = 21      #x轴坐标每21天显示一次
line_chart.x_labels_major = dates[::N]
line_chart.add('收盘价',close)
line_chart.render_to_file('收盘价折线图(￥).svg')
