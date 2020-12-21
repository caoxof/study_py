import requests
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

from requests.models import stream_decode_response_unicode
#执行API调用并存储响应
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
#print(r)                ##<response [200]>请求成功
#print(r.status_code)    ##status_code=200 请求成功
response_dict = r.json()   ##API返回的是json格式,r.json()转换为字典
#print(response_dict.keys())  ##dict_keys(['total_count', 'incomplete_results', 'items'])
print("Total repositories:",response_dict['total_count'])
repo_dicts = response_dict['items']  ##仓库信息为字典中的字典
print("Repositories returned:", len(repo_dicts))
repo_dict = repo_dicts[0]
print("\nKeys:",len(repo_dict))
##print(repo_dict.keys())
##for key in sorted(repo_dict.keys()):
   # print(key)
#print("\nSelected information about first repository:")
"""
print("\nSelected information about each repository")
for repo_dict in repo_dicts:
    print('Name:',repo_dict['name'])
    print('Owner:',repo_dict['owner']['login'])
    print('Stars:',repo_dict['stargazers_count'])
    print('Repository:',repo_dict['html_url'])
    #print('Created:',repo_dict['created_at'])
    #print('Updated:',repo_dict['updated_at'])
    print('Description:',repo_dict['description'])
    print('#'*50)
"""
names, stars = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    stars.append(repo_dict['stargazers_count'])
#可视化
my_style = LS('#333366',base_style=LCS)
chart = pygal.Bar(style=my_style,x_label_rotation=45,show_legend=False)
chart.title = 'Most-Starred Python Projects on Github'
chart.x_labels = names
chart.add('',stars)
chart.render_to_file('python_repos.svg')

