'''
登录模块
展示登录窗口并实现登录功能
'''

import tkinter as tk
import gui.chat_dlg

class LoginDlg(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.__userName = ''
        self.__password = ''
        self.pack()
        self.createWidgets()
    
    @property
    def password(self):
        return self.__password

    @property
    def userName(self):
        return self.__userName

    def createWidgets(self):
        # 登录框架=============
        loginLF = tk.LabelFrame(self, text='登录')
        loginLF.grid(row=0, column=0)
        self.loginLF = loginLF#这里需要将它保存为属性，否则这个函数结束后会出问题

        # 用户名
        self.userNameLab = tk.Label(loginLF, text='用户名')
        self.userNameLab.grid(row=0, column=0)
        self.userNameEntry = tk.Entry(loginLF)
        self.userNameEntry.grid(row=0, column=1,columnspan=2)

        # 密码框
        self.passwdLab = tk.Label(loginLF, text='密码')
        self.passwdLab.grid(row=1, column=0)
        self.passwdEntry = tk.Entry(loginLF,show='*')
        self.passwdEntry.grid(row=1, column=1,columnspan=2)

        # 登录按钮
        self.loginBtn = tk.Button(loginLF, text='登录',command=self.toChatDlg)
        self.loginBtn.grid(row=2, column=1)

        # 注册按钮
        self.signupBtn = tk.Button(loginLF, text='注册')
        self.signupBtn.grid(row=2, column=2)

    def toChatDlg(self):
        gui.chat_dlg.ChatDlg()
        self.destroy()
        



if __name__ == '__main__':
    window = tk.Tk()
    loginDlg = LoginDlg(window)
    loginDlg.mainloop()

    