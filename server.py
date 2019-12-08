'''
simuqq的服务端，开启之后才可以登录成功
'''

import socket
import threading
import json
import utility
import time
import select
import logging
logging.basicConfig(level=logging.INFO)


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
        self.dataFile = 'account_database.json'
        self.bufsize = 2048  # 一次最大接收字节数
        # 在线账号
        self.onlineClients = {}  # 客户端字典，键是账号字符串

    def launch(self):
        '''
        启动服务器
        '''
        # 绑定地址
        self.serSock.bind((self.host, self.port))
        # 监听
        self.serSock.listen(20)
        # 创建连接线程
        #self.acceptThread = threading.Thread(target=self.acceptLoop)
        # self.acceptThread.start()
        self.selectLoop()

    def acceptLoop(self):
        '''
        接受连接的线程循环

        刚开始的时候测试客户端用的，
        客户端的登录测试完毕之后，将其中的代码提取出来封成另一个函数acceptLogin()，
        供selectLoop使用
        '''
        while True:
            logging.info('正在等待新的连接')
            # 接受新的连接请求
            cliSock, cliAddr = self.serSock.accept()
            self.acceptLogin(cliSock, cliAddr)

    def selectLoop(self):
        '''
        使用select函数来进行处理的循环
        '''
        readList = [self.serSock]
        writeList = []
        message_dict = {}  # 存储消息用的字典，键为socket，值为消息列表
        i = 0

        logging.info('服务器已经启动，正在等待客户端的连接')
        while True:
            logging.debug('循环数：'+str(i))
            i += 1
            # select函数阻塞timeout时间，从参数的三个列表中，选择出此时可读取、可写入、出现错误的元素返回
            readableList, writableList, exceptionList = select.select(
                readList, writeList, readList, 1)

            # 1. 遍历当前可读取的socket
            for sock in readableList:

                if sock is self.serSock:
                    # 如果是服务端socket，那么就是有客户端来连接了
                    cliSock, cliAddr = sock.accept()
                    if self.acceptLogin(cliSock, cliAddr) == 0:
                        # 如果登录成功
                        readList.append(cliSock)  # 将新的客户端socket加入监听列表
                        message_dict[cliSock] = []  # 为新的socket创建消息列表
                        self.refreshCurOnline()  # 给所有在线客户端刷新在线信息
                else:
                    # 已连接的用户发送消息过来
                    # 接收一下

                    try:
                        data = sock.recv(self.bufsize)
                    except:
                        # 如果收到空数据，代表客户端已经断开连接
                        readList.remove(sock)
                        del message_dict[sock]  # 删除对应的消息队列

                        logging.info('客户端[userName={}]断开了连接'.format(
                            self.getUserNameBySock(sock)))
                        self.closeLink(sock)
                    else:  # 如果没有出现异常，再检查是否收到空数据
                        if not data:
                            # 如果收到空数据，代表客户端已经断开连接
                            readList.remove(sock)
                            del message_dict[sock]  # 删除对应的消息队列
                            self.closeLink(sock)
                            print('客户端[{}]断开了连接'.format(
                                self.getUserNameBySock(sock)))
                        else:
                            # 收到老用户的消息
                            dataStr = data.decode()
                            # 将消息加入对应的消息队列
                            message_dict[sock].append(dataStr)
                            writeList.append(sock)

            # 2.处理待回复的消息
            for sock in writableList:
                while len(message_dict[sock]) > 0:
                    dataStr = message_dict[sock][0]  # 取出消息队列中第一个消息
                    del message_dict[sock][0]
                    self.addressMsg(sock, dataStr)  # 处理消息
                    # 测试代码：测试消息处理是否可用
                    # sock.sendall(('echo:'+dataStr).encode())

                # 将消息队列中所有消息处理完毕，则将它从待回复队列中删除
                writeList.remove(sock)

            # 3.处理出错的socket
            for sock in exceptionList:
                readList.remove(sock)

    def checkAccount(self, userName: str, password: str):
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
        # 发送错误消息
        if errStr != '':
            msgDict = {
                'type': 'err',
                'errStr': errStr
            }
            self.send(cliSock, **msgDict)

        # 删除该客户端
        for userName, accountInfo in list(self.onlineClients.items()):
            if accountInfo['socket'] == cliSock:
                del self.onlineClients[userName]  # 该客户端下线
        # 刷新其他客户端的在线列表数据
        self.refreshCurOnline()
        cliSock.close()  # 关闭此连接

    def send(self, cliSock: socket, **msgDict):
        '''
        向cliSock发送消息
        '''
        msgStr = utility.dumpJson(msgDict)
        cliSock.send(msgStr.encode())

    def sendLoginAck(self, cliSock):
        '''
        登录成功之后向客户端发送确认消息以及当前在线客户端列表
        '''
        curOnline = self.getCurOnline()  # 获取当前在线列表

        msgDict = {
            'type': 'login',
            'infoStr': '登录成功！',
            'data': curOnline,
            'userName': '',
            'password': ''
        }

        self.send(cliSock, **msgDict)

    def acceptLogin(self, cliSock, cliAddr):
        '''
        接受已连接的客户端的登录请求
        :return: 登录成功返回0，失败返回-1
        '''
        # 获取客户端提交的账号密码，客户端以json字符串的形式发送过来
        loginStr = cliSock.recv(self.bufsize).decode()
        loginDict = utility.loadJson(loginStr)

        # 检查登录消息是否正确
        if not utility.isCorrectMsg(loginDict):
            errStr = '数据有误，请重新连接'
            self.closeLink(cliSock, errStr)  # 关闭连接
            return -1

        # 检查账号
        cliUserName = loginDict['userName']
        cliPassword = loginDict['password']
        res = self.checkAccount(cliUserName, cliPassword)
        if res == -1:
            errStr = '账号不存在'
            self.closeLink(cliSock, errStr)  # 关闭连接
            return -1
        elif res == -2:
            errStr = '密码错误'
            self.closeLink(cliSock, errStr)  # 关闭连接
            return -1
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
            self.sendLoginAck(cliSock)
            return 0

    def addressMsg(self, sourceSock, msgStr: str):
        '''
        处理接收到的消息
        :param sourceSock: 消息源socket
        :param msgStr: 消息字符串
        :return: 处理成功返回0，出现错误返回-1
        '''
        # 解析消息
        msgDict = utility.loadJson(msgStr)
        if not utility.isCorrectMsg(msgDict):
            # 如果消息不合法
            return -1

        if msgDict['type'] == 'msg':
            # 如果是发送过来的聊天消息
            logging.info('[{}]对[{}]说：{}'.format(self.getUserNameBySock(
                sourceSock), msgDict['userName'], msgDict['message']))
            targetSock = self.getSockByUserName(msgDict['userName'])
            if targetSock == None:
                self.send(sourceSock, type='err', errStr='对方已经下线')
                return -1
            # 转发给对方
            msgDict['userName'] = self.getUserNameBySock(
                sourceSock)  # 将目的用户名改为源用户名
            self.send(targetSock, **msgDict)

    def getCurOnline(self):
        '''
        :return: 当前在线的账号数据dict，可直接作为消息的data键的值
        '''
        curOnline = {
            'curOnline': []
        }
        for client in self.onlineClients.keys():
            curOnline['curOnline'].append(client)
        return curOnline

    def refreshCurOnline(self):
        '''
        给所有在线的客户端发送数据刷新消息
        '''
        for userName, accountInfo in self.onlineClients.items():
            msgDict = {
                'type': 'data',
                'data': self.getCurOnline()
            }
            self.send(accountInfo['socket'], **msgDict)

    def getUserNameBySock(self, cliSock):
        '''
        :return: socket对应的当前在线的用户名,如果没找到，则返回空字符串
        '''
        for userName, accountInfo in list(self.onlineClients.items()):
            if accountInfo['socket'] == cliSock:
                return userName
        return ''

    def getSockByUserName(self, userName: str):
        '''
        :return: 用户名对应的socket,如果没找到，则返回None
        '''
        if userName in self.onlineClients.keys():
            return self.onlineClients[userName]['socket']
        else:
            return None


if __name__ == '__main__':
    server = Server(9999)
    server.launch()
