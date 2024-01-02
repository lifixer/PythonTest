import tkinter as tk
from socket import *
import threading
import queue
import json  # json.dumps(some)打包  json.loads(some)解包
import os
import os.path
import sys

IP = '127.0.0.1'
# IP = '192.168.1.103'(如果是多台主机，将IP改为服务器主机的地址即可)
PORT = 8087  # 端口
messages = queue.Queue()  # 存放总体数据
users = []  # 0:userName 2:str(Client_IP)  3:int(Client_PORT)定义一个二维数组
lock = threading.Lock()  # 线程锁，防止多个线程占用同个资源时导致资源不同步的问题
BUFLEN = 512


def Current_users():  # 统计当前在线人员，用于显示名单并发送消息
    current_suers = []
    for i in range(len(users)):
        current_suers.append(users[i][0])  # 存放用户相关名字
    return current_suers


class ChatServer(threading.Thread):
    global users, que, lock

    def __init__(self):  # 构造函数
        threading.Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)  # 用UDP连接

    # 接受来自客户端的用户名，如果用户名为空，使用用户的IP与端口作为用户名。如果用户名出现重复，则在出现的用户名依此加上后缀“2”、“3”、“4”……
    def receive(self):  # 接收消息,b'用户数据，(用户地址)
        while True:
            print('a')
            Info, addr = self.s.recvfrom(1024)  # 收到的信息
            print('b')
            Info_str = str(Info, 'utf-8')
            userIP = addr[0]
            userPort = addr[1]
            print(f'Info_str:{Info_str},addr:{addr}')
            if '~0' in Info_str:  # 群聊
                data = Info_str.split('~')
                print("data_after_slpit:", data)  # data_after_slpit: ['cccc', 'a', '0']
                message = data[0]  # data
                userName = data[1]  # name
                chatwith = data[2]  # 0
                message = userName + '~' + message + '~' + chatwith  # 界面输出用户格式
                print("message:", message)
                self.Load(message, addr)
            elif '~' in Info_str and '0' not in Info_str:  # 私聊
                data = Info_str.split('~')
                print("data_after_slpit:", data)  # data_after_slpit: ['cccc', 'a', 'destination_name']
                message = data[0]  # data
                userName = data[1]  # name
                chatwith = data[2]  # destination_name
                message = userName + '~' + message + '~' + chatwith  # 界面输出用户格式
                self.Load(message, addr)
            else:  # 新用户
                tag = 1
                temp = Info_str
                for i in range(len(users)):  # 检验重名，则在重名用户后加数字
                    if users[i][0] == Info_str:
                        tag = tag + 1
                        Info_str = temp + str(tag)
                users.append((Info_str, userIP, userPort))
                print("users:", users)  # 用户名和信息[('a', '127.0.0.1', 65350)]
                Info_str = Current_users()  # 当前用户列表
                print("USERS:", Info_str)  # ['a']
                self.Load(Info_str, addr)
        # 在获取用户名后便会不断地接受用户端发来的消息（即聊天内容），结束后关闭连接。

    # 将地址与数据（需发送给客户端）存入messages队列。
    def Load(self, data, addr):
        lock.acquire()
        try:
            messages.put((addr, data))
            print(f"Load,addr:{addr},data:{data}")
        finally:
            lock.release()

    # 服务端在接受到数据后，会对其进行一些处理然后发送给客户端，如下图，对于聊天内容，服务端直接发送给客户端，而对于用户列表，便由json.dumps处理后发送。
    def sendData(self):  # 发送数据
        print('send')
        while True:
            if not messages.empty():  # 如果信息不为空
                message = messages.get()
                print("messages.get()", message)
                if isinstance(message[1], str):  # 判断类型是否为字符串
                    print("send str")
                    for i in range(len(users)):
                        data = ' ' + message[1]
                        print("send_data:", data.encode())  # send_data:b' a:cccc~a~------Group chat-------'
                        self.s.sendto(data.encode(), (users[i][1], users[i][2]))  # 聊天内容发送过去

                if isinstance(message[1], list):  # 是否为列表
                    print("message[1]", message[1])  # message[1]为用户名 message[0]为地址元组
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            self.s.sendto(data.encode(), (users[i][1], users[i][2]))
                            print("send_already")
                        except:
                            pass
        print('out_send_loop')

    def run(self):
        self.s.bind((IP, PORT))  # 绑定端口
        q = threading.Thread(target=self.sendData)  # 开启发送数据线程
        q.start()
        t = threading.Thread(target=self.receive)  # 开启接收信息进程
        t.start()


# 入口
if __name__ == '__main__':
    print('start')
    cserver = ChatServer()
cserver.start()
# netstat -an|find /i "50000"
