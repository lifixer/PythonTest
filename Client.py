from socket import *
import time
import tkinter
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText

IP = '127.0.0.1'
SERVER_PORT = 50000
user = ''
listbox1 = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = '0'  # 聊天对象
chat_pri = ''



# 登陆窗口的界面实现
root0 = tkinter.Tk()
root0.geometry("300x150")
root0.title('用户登陆窗口')
root0.resizable(0, 0)
one = tkinter.Label(root0, width=300, height=150, bg="#F5DE83")
one.pack()
IP = tkinter.StringVar()
IP.set('')
PORT = tkinter.StringVar()
PORT.set('')
USER = tkinter.StringVar()
USER.set('')
##将填空处内容和实际参数绑定起来 比如将输入的IP地址绑定到entryIP，以供后续使用
labelIP = tkinter.Label(root0, text='目的IP地址', bg="#F5DE83")   #bg代表颜色
labelIP.place(x=20, y=5, width=100, height=40)
entryIP = tkinter.Entry(root0, width=60, textvariable=IP)
entryIP.place(x=120, y=10, width=100, height=30)

labelPORT = tkinter.Label(root0, text='目的端口号', bg="#F5DE83")
labelPORT.place(x=20, y=40, width=100, height=40)
entryPORT = tkinter.Entry(root0, width=60, textvariable=PORT)
entryPORT.place(x=120, y=45, width=100, height=30)

labelUSER = tkinter.Label(root0, text='用户名', bg="#F5DE83")
labelUSER.place(x=20, y=75, width=100, height=40)
entryUSER = tkinter.Entry(root0, width=60, textvariable=USER)
entryUSER.place(x=120, y=80, width=100, height=30)


#界面完成后，以下就是编写实际的登录函数
def Login():
    global IP, PORT, user
    IP = entryIP.get()	#获取前面绑定的IP地址，PORT,user信息
    PORT = entryPORT.get()
    user = entryUSER.get()
    if not IP:
        tkinter.messagebox.showwarning('warning', message='目的IP地址为空!')  # 目的IP地址为空则提示
    elif not PORT:
        tkinter.messagebox.showwarning('warning', message='目的端口号为空!')  # 目的端口号为空则提示
    elif not user:
        tkinter.messagebox.showwarning('warning', message='用户名为空!')     # 客户端用户名为空则提示
    else:
        root0.destroy()	#提交后，登录窗口要自己销毁，以便进入登录成功后的界面

#登录按钮的实现
loginButton = tkinter.Button(root0, text="登录", command=Login, bg="#FF8C00")
loginButton.place(x=135, y=120, width=40, height=25)
root0.bind('<Return>', Login)	#将按钮与Login()函数绑定

root0.mainloop()


# 聊天窗口界面的实现
root1 = tkinter.Tk()
root1.geometry("640x480")
root1.title('聊天工具')
root1.resizable(0, 0)

## 聊天窗口中的消息界面的实现
listbox = ScrolledText(root1)
listbox.place(x=5, y=0, width=485, height=320)
listbox.tag_config('tag1', foreground='blue', backgroun="white")
listbox.insert(tkinter.END, '欢迎用户 '+user+' 加入聊天室!', 'tag1')
listbox.insert(tkinter.END, '\n')
# 聊天窗口中的在线用户列表界面的实现
listbox1 = tkinter.Listbox(root1)
listbox1.place(x=490, y=0, width=140, height=320)
# 聊天窗口中的聊天内容输入框界面的实现
INPUT = tkinter.StringVar()
INPUT.set('')
entryIuput = tkinter.Entry(root1, width=120, textvariable=INPUT)
entryIuput.place(x=5, y=330, width=485, height=140)



#UDP连接部分
ip_port = (IP, int(PORT))
s = socket(AF_INET, SOCK_DGRAM)
if user:
    s.sendto(user.encode(), ip_port)  # 发送用户名
else:           #e这部分else可删除，因为已经确保用户名不为空了
    s.sendto('用户名不存在', ip_port)
    user = IP + ':' + PORT

#发送聊天内容的函数实现，与下面的“发送按钮”绑定起来
def send():
    message = entryIuput.get() + '~' + user + '~' + chat
    s.sendto(message.encode(), ip_port)
    print("already_send message:",message)
    INPUT.set('')
    return 'break'  #按回车后只发送不换行

# 私聊窗口的函数实现
def Priva_window():
    chat_pri = entryPriva_target.get()
    message = entryPriva_talk.get()
    if not chat_pri:
        tkinter.messagebox.showwarning('warning', message='私聊目标名称为空!')  # 目的IP地址为空则提示
    else:
        root3.destroy()
        print("chat_pri", chat_pri)
        #print("message", message)message
        message = message + '~' + user + '~' + chat_pri
        #message = entryIuput.get() + '~' + user + '~' + chat_pri
        s.sendto(message.encode(), ip_port)
        INPUT.set('')

# 私聊窗口的界面实现。为什么私聊窗口界面要在函数里实现？因为他是要点击后自己跳出来，而不是一开始就存在的。
def Priva_Chat():
    global chat_pri,root3,window,Priva_target,labelPriva_target,entryPriva_target,Priva_talk,labelPriva_talk,entryPriva_talk
    root3 = tkinter.Toplevel(root1)
    root3.geometry("300x150")
    root3.title('私聊对象')
    root3.resizable(0, 0)
    window = tkinter.Label(root3, width=300, height=150, bg="LightBlue")
    window.pack()
    Priva_target = tkinter.StringVar()
    Priva_target.set('')
    labelPriva_target = tkinter.Label(root3, text='私聊用户名称', bg="LightBlue")
    labelPriva_target.place(x=20, y=5, width=100, height=40)
    entryPriva_target = tkinter.Entry(root3, width=60, textvariable=Priva_target)
    entryPriva_target.place(x=120, y=10, width=100, height=30)

    Priva_talk = tkinter.StringVar()
    Priva_talk.set('')
    labelPriva_talk = tkinter.Label(root3, text='私聊内容', bg="LightBlue")
    labelPriva_talk.place(x=20, y=40, width=100, height=40)
    entryPriva_talk = tkinter.Entry(root3, width=60, textvariable=Priva_talk)
    entryPriva_talk.place(x=120, y=45, width=100, height=30)

    Priva_targetButton = tkinter.Button(root3, text="确定", command=Priva_window, bg="Yellow")
    Priva_targetButton.place(x=135, y=120, width=40, height=25)

# “发送按钮”的界面实现，与send()函数绑定
sendButton = tkinter.Button(root1, text="发送", anchor='n', command=send, font=('Helvetica', 18), bg='white')
sendButton.place(x=535, y=350, width=60, height=40)
# “私聊发送按钮”的界面实现，与send()函数绑定，send通过text内容判断是私聊还是群发
PrivaButton = tkinter.Button(root1, text="私聊", anchor='n', command=Priva_Chat, font=('Helvetica', 18), bg='white')
PrivaButton.place(x=535, y=400, width=60, height=40)
root1.bind('<Return>', send)

# 接收信息的函数实现
def receive():
    global uses
    while True:
        data = s.recv(1024)
        data = data.decode()
        print("rec_data:",data)
        try:
            uses = json.loads(data)
            listbox1.delete(0, tkinter.END)
            listbox1.insert(tkinter.END, "       当前在线用户:")	#往用户列表插入信息
            #listbox1.insert(tkinter.END, "------Group chat-------")
            for x in range(len(uses)):
                listbox1.insert(tkinter.END, uses[x])
            users.append('------Group chat-------')
        except:
            data = data.split('~')
            print("data_after_slpit:",data) #data_after_slpit: ['cccc', 'a', '0/1']
            userName = data[0]   #data 
            userName = userName[1:]	#获取用户名
            message = data[1]  #信息
            chatwith = data[2]  #destination 判断是群聊还是私聊
            message = '  ' + message + '\n'
            recv_time = " "+userName+"   "+time.strftime ("%Y-%m-%d %H:%M:%S", time.localtime()) + ': ' + '\n'	#信息发送时间
            listbox.tag_config('tag3', foreground='green')
            listbox.tag_config('tag4', foreground='blue')
            if chatwith == '0':  # 群聊
                listbox.insert(tkinter.END, recv_time, 'tag3')
                listbox.insert(tkinter.END, message)
            elif chatwith != '0':  # 私聊别人或是自己发出去的私聊
                if userName == user:                     #如果是自己发出去的,用私聊字体显示
                    listbox.insert(tkinter.END, recv_time, 'tag3')
                    listbox.insert(tkinter.END, message, 'tag4')
                if chatwith == user:                                    #如果是发给自己的，用绿色字体显示
                    listbox.insert(tkinter.END, recv_time, 'tag3')
                    listbox.insert(tkinter.END, message, 'tag4')

            listbox.see(tkinter.END)


r = threading.Thread(target=receive)
r.start()  # 开始线程接收信息

root1.mainloop()
s.close()
