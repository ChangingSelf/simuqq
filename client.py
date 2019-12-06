
'''
simuqq的客户端
'''
import socket

class Client:
    def __init__(self):
        self.cliSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def connect(self,host,port):
        # 连接
        try:
            self.cliSock.connect((host,port))
        except:
            print('无法连接至目标主机，可能是目标主机服务未开启')
            return
        print('连接成功')
        self.cliSock.send('hello'.encode())

if __name__ == '__main__':
    client = Client()
    
    client.connect('127.0.0.1',9999)
    