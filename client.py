
'''
simuqq的客户端
'''
import socket
import json
import time
import gui.login_dlg
import utility
import tkinter as tk


class Client:
    def __init__(self, host:str, port:int):
        # 初始化socket
        self.cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        # 初始化配置
        self.dataFile = 'data\\account_database.json' #数据文件路径
        self.bufsize = 2048  # 一次最大接收字节数
        # 初始化界面
        self.window = tk.Tk()
        self.loginDlg = gui.login_dlg.LoginDlg(
            self.login, self.register, self.window)
        # 启动登录界面
        self.window.mainloop()

    def connect(self):
        # 连接
        
        try:
            self.cliSock.connect((self.host, self.port))
        except:
            utility.showerror('无法连接至目标主机，可能是目标主机服务未开启')
            
            return -1
        #测试用的输出
        print('连接成功')
        return 0

    def login(self):
        # 从登录对话框获取信息
        userName = self.loginDlg.userName.get()
        password = self.loginDlg.password.get()

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
        accountData = {
            'userName': userName,
            'password': password
        }
        accountStr = json.dumps(accountData)
        self.send(accountStr)

        # 如果发送信息成功，且账号信息正确，则弹出好友列表页面

        # 等待服务端的确认信息
        res = self.recv()
        try:
            res = json.loads(res)
        except:
            self.resetSock()
            return -1
        if 'errStr' in res.keys():
            utility.showerror(res['errStr'])
            self.resetSock()#重启socket
            return -1
        else:
            utility.showinfo('登录成功')
            return 0


    def register(self):
        '''
        注册
        在填写了用户名和密码之后，如果信息合法，则将信息写入数据文件
        '''
        # 从登录对话框获取信息
        userName = self.loginDlg.userName.get()
        password = self.loginDlg.password.get()

        # 检查合法性
        if userName == '':
            utility.showerror('用户名不能为空')
            return
        if password == '':
            utility.showerror('密码不能为空')
            return

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
                return

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
        self.cliSock.close()#连接错误，主动关闭
        self.cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9999
    client = Client(host, port)
