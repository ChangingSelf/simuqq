'''
simuqq主页面
'''
import tkinter as tk


class HomePage(tk.Frame):
    def __init__(self, selectCallback, master=None):
        super().__init__(master=master)
        # self.pack()
        self.master = master
        self.geometry()

        self.selectCallback = selectCallback  # 双击选择列表项时的回调函数
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
        self.userNameLab = tk.Label(profileLF, textvariable=self.userName)
        self.userNameLab.grid(row=0, column=1)

        # 好友列表框架==================
        contactLF = tk.LabelFrame(self, text='现在在线的其他人')
        contactLF.grid(row=1, column=0)
        self.contactLF = contactLF

        # 好友列表
        self.contactList = tk.Listbox(contactLF)
        self.contactList.grid(row=0, column=0)

        # 绑定双击事件
        self.contactList.bind('<Double-Button-1>', func=self.selectCallback)

    def geometry(self):
        self.master.geometry('300x400')

    def refreshList(self, curOnlineList):
        '''
        刷新列表显示
        '''
        # 先清空列表
        self.contactList.delete(0, tk.END)
        # 再加入列表
        for item in curOnlineList:
            if str(item) != self.userName.get():
                self.contactList.insert(tk.END, str(item))

    def getCurSelect(self):
        index = self.contactList.curselection()[0]
        return self.contactList.get(index)


if __name__ == '__main__':
    window = tk.Tk()
    homepage = HomePage(window)
    window.mainloop()
