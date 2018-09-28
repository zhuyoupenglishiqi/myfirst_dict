# #!/usr/bin/python3
# #coding:utf-8

# from socket import *
# import sys

# #创建网络连接
# def main():
#     if len(sys.argv) < 3:
#         print('argv is error')
#         return
#     HOST = sys.argv[1]
#     PORT = int(sys.argv[2])
#     s = socket()
#     try:
#         s.connect((HOST,PORT))
#     except Exception as e:
#         print(e)
#         return

#     #连接成功，进入一级界面
#     while True:
#         print('''
#             =====================
#             1.注册  2.登录  3.退出
#             =====================''')
#         cmd = input('输入选项:')



from socket import *
import sys
import getpass
import time

#创建连接
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    s = socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return

    #进入一级界面
    while True:
        print('''
            ====================
            1.注册  2.登录  3.退出
            ====================''')
        cmd = input('选择:')
        if cmd == '1':
            do_register(s)
        elif cmd == '2':
            do_login(s)
        elif cmd == '3':
            s.send('Q'.encode())
            sys.exit('退出')
        else:
            print('请正确操作！')
            continue

def do_register(s):
    while True:
        name = input('请输入用户名:')
        password = getpass.getpass()
        password1 = getpass.getpass('请确认密码:')

        if (' ' in name ) or (' ' in password):
            print('用户名和密码不允许有空格')
            continue
        if password != password:
            print('两次输入不一致')
            continue

        s.send(str('R '+name+' '+password).encode())
    
        data = s.recv(1023).decode()
        if data == 'OK':
            print('注册成功!')
            break
        else:
            print(data)
            return

def do_login(s):
    while True:
        name = input('user:')
        passward = getpass.getpass()
        s.send(str('L '+name+' '+passward).encode())
        data = s.recv(1025).decode()
        if data == 'OK':
            print('登录成功，即将跳转到二级界面')
            time.sleep(1)
            do_operate(s,name)
            break   
        else:
            print(data)
            continue

def do_operate(s,name):
    while True:
        print('''
            ================================
            1.查单词  2.查看历史记录  3.退出
            ================================''')
        cmd = input('选择:')
        if cmd == '1':
            do_query(s,name)
        elif cmd == '2':
            do_record(s,name)
        elif cmd == '3':
            print('退出')
            break

def do_query(s,name):
    while True:
        word = input('输入要查找的单词:')
        if not word:
            break
        s.send(str('find '+name+' '+word).encode())
        data = s.recv(1024).decode()
        print(data)

def do_record(s,name):
    s.send(str('record '+name).encode())
    data = s.recv(4096).decode()
    data = data.split('**')
    for t in data:
        print(t)
if __name__ == '__main__':
    main()