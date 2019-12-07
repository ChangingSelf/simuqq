'''
一些工具函数
'''
import tkinter.messagebox
import json

def showerror(errStr:str):
    '''
    显示错误对话框
    '''
    tkinter.messagebox.showerror(title='警告', message=errStr)

def showinfo(infoStr:str):
    '''
    显示错误对话框
    '''
    tkinter.messagebox.showinfo(title='信息', message=infoStr)

def resolveJsonStr(jsonStr:str):
    '''
    解析json字符串，进行错误处理
    :return:解析出的dict，如果不是规定的格式，解析出错时返回空dict
    '''
    try:
        jsonDict = json.loads(jsonStr)
    except:
        jsonDict = {}

    if not isinstance(jsonDict,dict):
        #保证返回的内容是字典
        jsonDict = {}

    return jsonDict






if __name__ == '__main__':
    res = resolveJsonStr('{}')
    print(res)