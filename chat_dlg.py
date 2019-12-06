'''
聊天对话框
'''
import tkinter as tk
from tkinter.scrolledtext import *

class ChatDlg(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # 聊天框架(包括输入框和输出框)==============
        chatLF = tk.LabelFrame(self, text='聊天框')
        chatLF.grid(row=0, column=0)
        self.chatLF = chatLF
        # 输出框
        self.outputTxt = ScrolledText(chatLF)
        self.outputTxt.grid(row=0,column=0)
        # 输入框
        self.inputTxt = ScrolledText(chatLF,height = 5)
        self.inputTxt.grid(row=1,column=0)


if __name__ == '__main__':
    window = tk.Tk()
    chatDlg = ChatDlg(window)
    chatDlg.mainloop()
