'''
simuqq主页面
主要是好友列表
'''
import tkinter as tk


class HomePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        #self.pack()
        self.userName = tk.StringVar()
        self.createWidgets()

    def createWidgets(self):
        # 个人信息框架=================
        profileLF = tk.LabelFrame(self, text='个人信息')
        profileLF.grid(row=0, column=0)
        self.profileLF = profileLF

        # 个人信息标签
        self.profileLab = tk.Label(profileLF, text='账号:')
        self.profileLab.grid(row=0, column=0)
        self.userNameLab = tk.Label(profileLF,textvariable=self.userName)
        self.userNameLab.grid(row=0, column=1)

        # 好友列表框架==================
        contactLF = tk.LabelFrame(self, text='好友列表')
        contactLF.grid(row=1, column=0)
        self.contactLF = contactLF

        # 好友列表
        self.contactList = tk.Listbox(contactLF)
        self.contactList.grid(row=0,column=0)


if __name__ == '__main__':
    window = tk.Tk()
    homepage = HomePage(window)
    window.mainloop()
    