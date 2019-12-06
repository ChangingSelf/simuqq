'''
simuqq的服务端，开启之后才可以登录成功
'''

import socket
import client_data  # 用于保存客户端的数据
import threading
import json


class Server:
    def __init__(self, port):
        '''
        :param port:服务器监听的端口号
        '''
        self.port = port
        self.host = '127.0.0.1'
        self.serSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientDict = {}  # 客户端字典，键是账号字符串，值是ClientData

    def launch(self):
        # 绑定地址
        self.serSock.bind((self.host, self.port))
        # 监听
        self.serSock.listen(20)
        # 创建连接线程
        self.acceptThread = threading.Thread(target=self.accept_loop)
        self.acceptThread.start()

    def accept_loop(self):
        '''
        接受连接的线程循环
        '''
        while True:
            print('正在等待新的连接')
            # 接受新的连接请求
            cliSock, cliAddr = self.serSock.accept()
            # 获取客户端提交的账号密码，客户端以json字符串的形式发送过来
            cliUserData = cliSock.recv(1024)
            try:
                cliUserData = json.loads(cliUserData)
                cliUserName = cliUserData['userName']
                cliPassword = cliUserData['password']
            except:
                # 如果发送过来的数据没有按照格式，那么给客户端发送错误信息
                errStr = '数据有误，请重新连接'
                self.closeLink(self, cliSock, errStr)  # 关闭连接
                continue

            # 检查账号
            res = self.checkAccount(cliUserName, cliPassword)
            if res == -1:
                errStr = '账号不存在'
                self.closeLink(cliSock, errStr)  # 关闭连接
            elif res == -2:
                errStr = '密码错误'
                self.closeLink(cliSock, errStr)  # 关闭连接
            else:
                cliSock.send('登录成功'.encode())

    def checkAccount(self, userName, password):
        '''
        检查账号信息是否正确
        :return 无误返回0，用户名不存在返回-1，密码错误返回-2
        '''
        # 预处理
        userName = userName.strip()
        password = password.strip()

        # 读取数据
        with open('account_database.json', 'w') as fp:
            accountData = json.load(fp)

        # 核对信息
        if userName not in accountData:
            # 如果不能找到用户名
            return -1  # 账号不存在

        if accountData[userName] != password:
            return -2 # 密码不正确

        return 0

    def closeLink(self, cliSock, errStr=''):
        '''
        关闭连接
        '''
        if errStr != '':
            cliSock.send(errStr.encode())
        cliSock.close()  # 关闭此连接


if __name__ == '__main__':
    server = Server(9999)
    server.launch()
    