import requests
from operator import itemgetter
from requests.models import Response
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print('Status Code:',r.status_code)

submission_ids = r.json()
submission_dicts = []
names = []
i = 1
for submission_id in submission_ids[:20]:
    url = ('https://hacker-news.firebaseio.com/v0/item/'+ str(submission_id)+'.json')
    submission_r = requests.get(url)
    print(i,'==>',submission_r.status_code)
    i +=1
    response_dict = submission_r.json()
    submission_dict ={
        'value' : response_dict.get('descendants',0),   ##dict.get 返回相关值，不存在时返回指定值。
        'label' : response_dict['title'],
#        'type' : response_dict['type'],
        'xlink' : 'https://news.ycombinator.com/item?id=' + str(submission_id)
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts,key=itemgetter('value'),reverse=True)

for submission_dict in submission_dicts:
    name = submission_dict['label']
    print('#'*40)
    print('Title :', submission_dict['label'])
    print('Discussion link :', submission_dict['xlink'])
    print('Comments :', submission_dict['value'])
    names.append(name)

"""
##图标样式配置
my_config = pygal.Config()               ##Config()-class实例
my_config.x_label_rotation = 45          ##x标签旋转45°
my_config.show_legend = False            ##是否显示图例
my_config.print_values = True
my_config.print_values_position = 'top'
my_config.pretty_print = True
my_config.truncate_label = 15            ##截断标签字符数
my_config.show_y_guides = False          ##是否显示y轴参考线
my_config.width = 1000
######pygal 2.0.0变动Move font_size config to style.
my_config.style = LS('#333366',base_style=LCS)
my_config.style.title_font_size = 24           ##图标标题字号
my_config.style.label_font_size = 14           ##副标签字号
my_config.style.major_label_font_size = 18     ##主标签字号
"""
###########################################################
chart_config = {
    "human_readable": True,
    "pretty_print": True,
    "truncate_legend": -1,
    "value_font_size": 15,
    "print_values": True,
    "show_legend": False,
    "print_values_position": "top",
    "print_labels": True,
    "value_formatter": lambda x: "{0: .2f}".format(x),
}
style_config = {
    "font_family": "googlefont:lato",
    "plot_background": "white",
    "value_font_size": 15,
    "show_y_guides": False,
    "show_y_labels": False,
    "colors": ("#0099d6", "#0099d6", "#0099d6", "#0099d6", "#0099d6", "#6d6f71", "#6d6f71"),
}
###########################################################
#chart = pygal.Bar(my_config)
chart = pygal.Bar(style= [style_config], config= [chart_config])
chart.title = 'HACKER-NEWS.FIREBASEIO.TOPSTORIES'
chart.x_labels = names
chart.add('',submission_dicts)
chart.render_to_file('Topstories01.svg')


