import pymysql
try:
    db = pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='经营',port=3307,charset='utf8')
    # 检验数据库是否连接成功
    cursor = db.cursor()
    # 这个是执行sql语句，返回的是影响的条数
    data = cursor.execute('SELECT * FROM `b2合同信息`')
    data_title = cursor.description
    # 得到一条数据
#    one = cursor.fetchone()
    print(data_title)
    print(data)
    print('#'*50)
#    print(one)

except pymysql.Error as e :
    print(e)
    print('操作数据库失败')
finally:
     # 如果连接成功就要关闭数据库
    if db:
        db.close()

# 将一条数据转成字典方便查找
new = dict(zip([x[0] for x in cursor.description],[x for x in cursor.fetchone()]))
print(new)

print(new.keys())
print(new.values())
# 将多条数据转成字典类型
print('-----------')


def new2dict(new):
    return dict(zip([x[0] for x in cursor.description],[x for x in new]))
news_list = list(map(new2dict,cursor.fetchall()))
#print(news_list)
# 把上面的第一条数据插进去这个列表
news_list.insert(0,new)
#print(news_list)
# 查询某一条数据
def lenght(tt):
    length = len(tt)
    utf8_length = len(tt.encode('utf-8'))
    length = (utf8_length - length)/2 + length  # float
    return int(length)

for i in range(60):
    pr1 = i+1
    pk1 = 3-len(str(pr1))             #序号占位5个字符
    pr2 = str(news_list[i]['签订时间'])
    pk2 = 15-len(pr2)                 #'签订时间'占位12
    pr3 = str(news_list[i]['项目简称'])
    pk3 = 25-lenght(pr3)                 #'签订时间'占位20
    pr4 = str(news_list[i]['合同额(元)'])
    pk4 = 12-len(pr4)                 #'签订时间'占位8
    print('*',' '*pk1,pr1,'*',' '*pk2,pr2,'*',' '*pk3,pr3,'*',' '*pk4,pr4,'*',sep='')
