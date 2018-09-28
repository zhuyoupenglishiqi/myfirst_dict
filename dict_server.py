'''
name:zhu
date:2018/9/27
email:850273779@qq.com
modules:pymysql
this is a dict 
'''

from socket import *
import os,time,signal,pymysql,sys

#定义需要的全局变量
dict_path = './dict.txt'
HOST = '0.0.0.0'
PORT = 9999
ADDR = (HOST,PORT)

def do_child(c,db):
    while True:
        data = c.recv(1024).decode()
        if not data:
            break
        data_list = data.split()
        if data_list[0] == 'R':
            do_register(c,db,data_list[1],data_list[2])
        elif data_list[0] == 'L':
            do_login(c,db,data_list[1],data_list[2])
        elif data == 'Q':
            print('允许退出')
        elif data_list[0] == 'find':
            do_query(c,db,data_list[1],data_list[2])
        elif data_list[0] == 'record':
            do_hist(c,db,data_list[1])


def do_register(c,db,name,password):
    cursor = db.cursor()
    sql_select = 'select name from user \
    where name ="%s"'%name
    cursor.execute(sql_select)
    data1 = cursor.fetchone()
    if data1 != None:
        c.send('该用户已存在!'.encode())
        return

    #将用户信息插入数据库
    sql = 'insert into user (name,password) \
    values("%s","%s")'%(name,password)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    c.send('OK'.encode())

def do_login(c,db,name,passwd):
    cursor = db.cursor()
    sql_select = 'select name,password from user \
    where name = "%s" and password = "%s"'%(name,passwd)
    cursor.execute(sql_select)
    data1 = cursor.fetchone()
    if data1 != None:
        c.send('OK'.encode())
    else:
        c.send('用户名或者密码错误'.encode())

def do_query(c,db,name,word):
    cursor = db.cursor()
    sql_insert = 'insert  into  record (name,word)\
    values("%s","%s")'%(name,word)
    try:
        cursor.execute(sql_insert)
        db.commit()
    except:
        db.rollback()

    sql_select = 'select interpret from words \
    where word = "%s"'%word
    cursor.execute(sql_select)
    data1 = cursor.fetchone()
    if data1 != None:
        data = data1[0]
        c.send(data.encode())
    else:
        c.send('没有此单词'.encode())

def do_hist(c,db,name):
    cursor = db.cursor()
    sql_select = 'select * from record \
    where name = "%s"'%name
    cursor.execute(sql_select)
    data1 = cursor.fetchall()
    for t in data1:
        c.send(str(str(t)+'**').encode())
    c.send('###'.encode())


#流程控制
def main():
    #创建数据库连接
    db = pymysql.connect \
    ('localhost','root','123456','dict')

    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #忽略子进程信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    #等待客户端连接，并创建子进程
    while True:
        try:
            c,addr = s.accept()
            print('connect from:',addr)
        except KeyboardInterrupt: #ctrl+c 退出
            s.close()
            sys.exit('服务器退出')
        except Exception as e: #打印异常，继续等待客户端连接
            print(e)
            continue

        #没有异常，则创建子进程
        pid = os.fork()
        if pid == 0:
            do_child(c,db)

        else:
            c.close()
            continue


if __name__ == '__main__':
    main()