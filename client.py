
'''
simuqq的客户端
'''
import socket
import sys
import threading
import json
import time
import gui.login_dlg
import gui.home_page
import gui.chat_dlg
import utility
import tkinter as tk


class Client:
    def __init__(self, host: str, port: int):
        # 初始化属性
        self.cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.chatWith = ''  # 聊天的对象的用户名

        # 初始化配置
        self.dataFile = 'account_database.json'  # 数据文件路径
        self.bufsize = 2048  # 一次最大接收字节数
        # 初始化界面
        self.window = tk.Tk()  # 主窗口
        self.window.title('SimuQQ登录界面')
        self.window.protocol("WM_DELETE_WINDOW", self.quit)  # 按右上角关闭即关闭程序
        self.window.resizable(0, 0)  # 不可改变大小

        self.chatWindow = tk.Toplevel(self.window)
        self.chatWindow.protocol(
            "WM_DELETE_WINDOW", self.hideChatWindow)  # 右上角关闭即隐藏聊天窗口
        self.gui = {
            'loginDlg': gui.login_dlg.LoginDlg(
                self.login, self.register, self.window),
            'homePage': gui.home_page.HomePage(self.chat, self.window),
            'chatDlg': gui.chat_dlg.ChatDlg(self.sendChatMsg, self.chatWindow)
        }
        self.gui['loginDlg'].grid(row=0, column=0)
        self.gui['loginDlg'].geometry()

        # 启动登录界面
        self.chatWindow.withdraw()
        self.window.mainloop()

    def quit(self):
        '''
        关闭程序
        '''
        # self.window.destroy()
        # for page in self.gui.keys():
        # self.gui[page].destroy()
        sys.exit(0)

    def hideChatWindow(self):
        '''
        隐藏聊天窗口
        '''
        self.chatWindow.withdraw()

    def connect(self):
        '''
        :return: 连接成功返回0，失败返回-1
        '''
        # 连接

        try:
            self.cliSock.connect((self.host, self.port))
        except:
            utility.showerror('无法连接至目标主机，可能是目标主机服务未开启')

            return -1
        # 测试用的输出
        # print('连接成功')
        return 0

    def login(self):
        '''
        登录
        :return: 登录成功返回0，失败返回-1
        '''
        # 从登录对话框获取信息
        userName = self.gui['loginDlg'].userName.get()
        password = self.gui['loginDlg'].password.get()

        # 检查合法性
        if userName == '':
            utility.showerror('用户名不能为空')
            return -1
        if password == '':
            utility.showerror('密码不能为空')
            return -1

        # 如果连接成功，向服务器发送信息
        res = self.connect()
        if res != 0:
            return -1
        # 构造并发送消息
        self.sendLoginData(userName, password)

        # 如果发送信息成功，且账号信息正确，则弹出好友列表页面

        # 等待服务端的确认信息
        if self.recvLoginAck() == 0:
            # 跳转到主页面
            self.userName = userName
            self.gotoHomePage()
            # 开启接收消息线程
            self.recvThread = threading.Thread(target=self.recvLoop)
            self.recvThread.setDaemon(True)
            self.recvThread.start()
        else:
            return -1

    def register(self):
        '''
        注册
        在填写了用户名和密码之后，如果信息合法，则将信息写入数据文件
        :return: 注册成功返回0,失败返回-1
        '''
        # 从登录对话框获取信息
        userName = self.gui['loginDlg'].userName.get()
        password = self.gui['loginDlg'].password.get()

        # 检查合法性
        if userName == '':
            utility.showerror('用户名不能为空')
            return -1
        if password == '':
            utility.showerror('密码不能为空')
            return -1

        with open(self.dataFile, 'a+') as fp:
            # 使用a+方式打开，防止文件内容被覆盖
            fp.seek(0)  # 调整指针到开头
            accountStr = fp.read()
            if accountStr == '':
                # 如果文件内没有内容，即刚刚创建
                accountData = {}
            else:
                # 否则读取文件内容
                fp.seek(0)
                accountData = json.loads(accountStr)

            if userName in accountData.keys():
                utility.showerror('该用户名已经被注册')
                return -1

            # 写入数据文件
            accountData.update({
                userName: {
                    'password': password,
                    'registerTime': time.time()
                }
            })

            utility.showinfo('注册成功！')
            fp.seek(0)
            fp.truncate()  # 只保留从开头到当前位置，其余删除
            json.dump(accountData, fp, indent=4, separators=(',', ':'))

        return 0

    def chat(self, event):
        '''
        与当前选中的客户端聊天
        '''
        # 获取当前用户名
        userName = self.gui['homePage'].getCurSelect()

        # 打开聊天窗口
        self.openChatWindow(userName)

    def openChatWindow(self, userName):
        '''
        打开聊天窗口
        :param userName: 聊天对象的用户名
        '''
        self.chatWith = userName  # 设置聊天对象
        self.gui['chatDlg'].grid(row=0, column=0)
        self.chatWindow.title('[{}]向[{}]发起的聊天'.format(self.userName, userName))
        self.chatWindow.deiconify()
        # self.chatWindow.mainloop()

    def sendChatMsg(self):
        '''
        发送聊天消息
        '''
        # 获取聊天窗口的输入框内文字
        chatMsg = self.gui['chatDlg'].getInputContent()

        # 构造消息
        msgDict = {
            'type': 'msg',
            'userName': self.chatWith,
            'message': chatMsg
        }
        msgStr = utility.dumpJson(msgDict)
        # 发送消息
        self.send(msgStr)
        # 同时在自己这边显示自己说的话
        # 构建输出内容
        outputContent = '[{}]{}\n{}'.format(
            self.userName, time.strftime('%Y/%m/%d %H:%M:%S'), chatMsg)

        self.gui['chatDlg'].addOutputContent(outputContent)
        # 清空输入框
        self.gui['chatDlg'].clearInputContent()

    def send(self, msg: str):
        '''
        向服务端发送消息
        :param msg:要发送的消息字符串
        '''
        self.cliSock.send(msg.encode())

    def recv(self):
        '''
        :return: 接收到的字符串
        '''
        return self.cliSock.recv(self.bufsize).decode()

    def resetSock(self):
        '''
        重新设置socket
        '''
        self.cliSock.close()  # 连接错误，主动关闭
        self.cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def gotoHomePage(self):
        '''
        跳转到主页面
        '''

        for page in self.gui.keys():
            self.gui[page].grid_forget()

        self.window.title('SimuQQ主页面')
        self.gui['homePage'].grid(row=0, column=0)
        self.gui['homePage'].userName.set(self.userName)
        self.gui['homePage'].geometry()

    def sendLoginData(self, userName: str, password: str):
        '''
        发送登录数据
        '''
        # 构造并发送消息
        accountData = {
            'type': 'login',
            'userName': userName,
            'password': password
        }
        accountStr = utility.dumpJson(accountData)
        self.send(accountStr)

    def recvLoginAck(self):
        '''
        等待服务端传回确认
        :return: 成功返回0，失败返回-1
        '''
        res = self.recv()
        res = utility.loadJson(res)
        # 检查消息合法性
        if not utility.isCorrectMsg(res):
            self.resetSock()
            return -1

        if res['type'] == 'err':
            # 如果收到的是服务端的错误消息
            utility.showerror(res['errStr'])
            self.resetSock()  # 重启socket
            return -1
        elif res['type'] == 'login':
            # 登录成功，输出信息
            if 'infoStr' in res.keys():
                utility.showinfo(res['infoStr'])
            else:
                utility.showinfo('登录成功')

            if 'data' in res.keys():
                self.contactList = res['data']['curOnline']
                self.gui['homePage'].refreshList(self.contactList)
            else:
                contactList = {}

            return 0
        else:
            # 如果不是err消息也不是确认消息，则登录失败
            self.resetSock()
            return -1

    def recvLoop(self):
        '''
        接收消息的循环
        '''
        while True:
            msgStr = self.recv()
            msgDict = utility.loadJson(msgStr)
            if not utility.isCorrectMsg(msgDict):
                continue  # 如果消息不正确，忽略这个消息

            if msgDict['type'] == 'data':
                # 如果接收到数据刷新消息
                self.contactList = msgDict['data']['curOnline']
                self.gui['homePage'].refreshList(self.contactList)
            if msgDict['type'] == 'msg':
                # 如果接收到聊天消息
                self.openChatWindow(msgDict['userName'])
                # 构建输出内容
                outputContent = '[{}]{}\n{}'.format(
                    msgDict['userName'], time.strftime('%Y/%m/%d %H:%M:%S'), msgDict['message'])

                self.gui['chatDlg'].addOutputContent(outputContent)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9999
    client = Client(host, port)
