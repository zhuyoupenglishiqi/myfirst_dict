# import pymysql
# import re

# f = open('dict.txt')

# #连接数据库中的dict库
# db = pymysql.connect('localhost','root','123456','dict')

# #生成游标
# cursor = db.cursor()

# for line in f:
#     l = re.split(r'\s+',line)
#     word = l[0]
#     interpret = ''.join(l[1:])
#     sql = 'insert into words \
#     (word,interpret) values("%s","%s")'%(word,interpret)

#     try:
#         cursor.execute(sql)
#         db.commit()
#     except:
#         db.rollback()
# f.close()


import pymysql
import re

#连接数据库中的ｄｉｃｔ库
db = pymysql.connect('localhost','root','123456','dict')

#打开文件dict.txt
with open('dict.txt') as f:
    #生成游标
    cursor = db.cursor()

    #读取dict.txt中的数据并保存到dict中的words表中
    for line in f:
        l = re.split(r'\s+',line)
        word = l[0]
        interpret = ' '.join(l[1:])
        sql = 'insert into words (word,interpret) \
        values("%s","%s")'%(word,interpret)

    #执行mysql语句
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
