
'''
simuqq的客户端
'''
import socket
import gui.login_dlg
import tkinter as tk

class Client:
    def __init__(self,host,port):
        self.cliSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = host
        self.port = port
        #初始化界面
        self.window = tk.Tk()
        self.loginDlg = gui.login_dlg.LoginDlg(self.login,self.register,self.window)
        #启动登录界面
        self.loginDlg.mainloop()


    def connect(self):
        # 连接
        try:
            self.cliSock.connect((self.host,self.port))
        except:
            print('无法连接至目标主机，可能是目标主机服务未开启')
            return
        print('连接成功')
        self.cliSock.send('hello'.encode())
    
    def login(self):
        self.connect()

    def register(self):
        pass

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9999
    client = Client(host,port)
    
    