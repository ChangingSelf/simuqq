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

def loadJson(jsonStr:str):
    '''
    将str转为dict
    :return:解析出的dict，如果不是规定的格式，解析出错时返回空dict
    '''
    jsonStr = str(jsonStr)
    try:
        jsonDict = json.loads(jsonStr)
    except:
        jsonDict = {}

    if not isinstance(jsonDict,dict):
        #保证返回的内容是字典
        jsonDict = {}

    return jsonDict

def dumpJson(jsonDict:dict):
    '''
    将dict转为str
    '''
    if not isinstance(jsonDict,dict):
        #如果传入的不是字典
        jsonDict = {}

    try:
        jsonStr = json.dumps(jsonDict)
    except:
        jsonStr = ''

    return jsonStr




if __name__ == '__main__':
    res = loadJson('')
    res = dumpJson('res')
    print(res)
    print(type(res))