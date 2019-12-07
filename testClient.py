'''
学习select使用的客户端
参考链接:https://www.jianshu.com/p/e26594304e11
'''
import socket

cliSock = socket.socket()
cliSock.connect(('127.0.0.1', 12346))

while True:
    sendStr = input('input>')
    cliSock.sendall(sendStr.encode())
    recvStr = cliSock.recv(1024).decode()
    print(recvStr)

cliSock.close()