'''
simuqq的服务端，开启之后才可以登录成功
'''

import socket
import threading
import json
import utility
import time
import logging
logging.basicConfig(level=logging.DEBUG)


class Server:
    def __init__(self, port):
        '''
        :param port:服务器监听的端口号
        '''
        # 初始化socket
        self.port = port
        self.host = '127.0.0.1'
        self.serSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 初始化配置
        self.dataFile = 'data\\account_database.json'
        # 在线账号
        self.onlineClients = {}  # 客户端字典，键是账号字符串

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
            logging.info('正在等待新的连接')
            # 接受新的连接请求
            cliSock, cliAddr = self.serSock.accept()
            # 获取客户端提交的账号密码，客户端以json字符串的形式发送过来
            loginStr = cliSock.recv(1024).decode()
            loginDict = utility.loadJson(loginStr)

            #检查登录消息是否正确
            if not utility.isCorrectMsg(loginDict):
                errStr = '数据有误，请重新连接'
                self.closeLink(cliSock, errStr)  # 关闭连接
                continue

            # 检查账号
            cliUserName = loginDict['userName']
            cliPassword = loginDict['password']
            res = self.checkAccount(cliUserName, cliPassword)
            if res == -1:
                errStr = '账号不存在'
                self.closeLink(cliSock, errStr)  # 关闭连接
            elif res == -2:
                errStr = '密码错误'
                self.closeLink(cliSock, errStr)  # 关闭连接
            else:
                logging.info('用户[userName={}]登录成功'.format(cliUserName))
                # 将新用户加入在线列表
                self.onlineClients.update({
                    cliUserName: {
                        'socket': cliSock,  # 客户端socket
                        'address': cliAddr,  # 客户端地址
                        'loginTime': time.time()  # 登录时间
                    }
                })
                # 登录成功，向该客户端发送确认消息
                self.sendAck(cliSock)

    def checkAccount(self, userName, password):
        '''
        检查账号信息是否正确
        :return 无误返回0，用户名不存在返回-1，密码错误返回-2
        '''
        # 预处理
        userName = userName.strip()
        password = password.strip()

        # 读取数据
        with open(self.dataFile, 'r') as fp:
            accountData = json.load(fp)

        # 核对信息
        if userName not in accountData:
            # 如果不能找到用户名
            return -1  # 账号不存在

        if accountData[userName]['password'] != password:
            return -2  # 密码不正确

        return 0

    def closeLink(self, cliSock, errStr=''):
        '''
        关闭连接
        '''
        if errStr != '':
            msgDict = {
                'errStr': errStr
            }
            self.send(cliSock, **msgDict)
        cliSock.close()  # 关闭此连接

    def send(self, cliSock: socket, **msgDict):
        
        msgStr = utility.dumpJson(msgDict)
        cliSock.send(msgStr.encode())

    def sendAck(self, cliSock):
        '''
        登录成功之后向客户端发送确认消息以及当前在线客户端列表
        '''
        curOnline = {
            'curOnline':[]
        }
        for client in self.onlineClients.keys():
            curOnline['curOnline'].append(client)
        
        msgDict = {
            'type':'login',
            'infoStr':'登录成功！',
            'data':curOnline,
            'userName':'',
            'password':''
        }

        self.send(cliSock,**msgDict)
        


if __name__ == '__main__':
    server = Server(9999)
    server.launch()
