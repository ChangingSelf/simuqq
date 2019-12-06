'''
登录模块
展示登录窗口并实现登录功能
'''

import tkinter as tk
import gui.chat_dlg

class LoginDlg(tk.Frame):
    def __init__(self, loginCallback,regCallback,master=None):
        super().__init__(master=master)
        self.master = master
        #设置按钮回调函数
        self.loginCallback = loginCallback
        self.regCallback = regCallback
        #初始化
        self.userName = tk.StringVar()#与文本框双向绑定
        self.password = tk.StringVar()
        self.pack()
        self.createWidgets()


    def createWidgets(self):
        # 登录框架=============
        loginLF = tk.LabelFrame(self, text='登录')
        loginLF.grid(row=0, column=0)
        self.loginLF = loginLF#这里需要将它保存为属性，否则这个函数结束后会出问题

        # 用户名
        self.userNameLab = tk.Label(loginLF, text='用户名')
        self.userNameLab.grid(row=0, column=0)
        self.userNameEntry = tk.Entry(loginLF,textvariable=self.userName)
        self.userNameEntry.grid(row=0, column=1,columnspan=2)

        # 密码框
        self.passwdLab = tk.Label(loginLF, text='密码')
        self.passwdLab.grid(row=1, column=0)
        self.passwdEntry = tk.Entry(loginLF,show='*',textvariable=self.password)
        self.passwdEntry.grid(row=1, column=1,columnspan=2)

        # 登录按钮
        self.loginBtn = tk.Button(loginLF, text='登录',command=self.loginCallback)
        self.loginBtn.grid(row=2, column=1)

        # 注册按钮
        self.signupBtn = tk.Button(loginLF, text='注册',command=self.regCallback)
        self.signupBtn.grid(row=2, column=2)

        
    def test(self):
        print(self.userName.get())
        print(self.password.get())


def test2():
    pass

if __name__ == '__main__':
    window = tk.Tk()
    loginDlg = LoginDlg(test2,test2,window)
    loginDlg.mainloop()

    