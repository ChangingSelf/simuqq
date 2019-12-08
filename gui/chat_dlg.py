'''
聊天对话框
'''
import tkinter as tk
from tkinter.scrolledtext import *


class ChatDlg(tk.Frame):
    def __init__(self, sendCallback, master=None):
        super().__init__(master=master)
        self.master = master
        self.sendCallback = sendCallback
        # self.pack()
        self.createWidgets()

    def createWidgets(self):
        # 聊天框架(包括输入框和输出框)==============
        chatLF = tk.LabelFrame(self, text='聊天框')
        chatLF.grid(row=0, column=0)
        self.chatLF = chatLF
        # 输出框
        self.outputTxt = ScrolledText(chatLF, state=tk.DISABLED)
        self.outputTxt.grid(row=0, column=0)
        # 输入框
        self.inputTxt = ScrolledText(chatLF, height=5)
        self.inputTxt.grid(row=1, column=0)
        # 发送按钮
        self.sendBtn = tk.Button(chatLF, text='发送', command=self.sendCallback)
        self.sendBtn.grid(row=2, column=0, sticky=tk.E)

    def getInputContent(self):
        return self.inputTxt.get(0.0, tk.END)

    def clearInputContent(self):
        self.inputTxt.delete(0.0, tk.END)

    def addOutputContent(self, content: str):
        self.outputTxt.config(state=tk.NORMAL)  # 先调整为可插入，插入完再设置为禁用
        self.outputTxt.insert(tk.INSERT, content+'\n')
        self.outputTxt.see(tk.END)  # 将滚动条位置移动到最末尾
        self.outputTxt.config(state=tk.DISABLED)


def test(self):
    pass


if __name__ == '__main__':
    window = tk.Tk()
    chatDlg = ChatDlg(test, window)
    chatDlg.mainloop()
