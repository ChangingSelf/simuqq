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

def isCorrectMsg(msg:dict):
    '''
    判断收到的消息是否符合规定
    :return: 不符合则返回False
    '''
    if not isinstance(msg,dict):
        #如果不是字典，不合法
        return False
    
    if 'type' not in msg.keys():
        #如果不含type字段，不合法
        return False
    
    # 每种类型的消息都有对应的必选字段
    if msg['type'] == 'login':
        if 'userName' not in msg.keys():
            return False
        if 'password' not in msg.keys():
            return False
    elif msg['type'] == 'data':
        if 'data' not in msg.keys():
            return False
        elif not isinstance(msg['data'],dict):
            return False
    elif msg['type'] == 'msg':
        if 'userName' not in msg.keys():
            return False
        if 'message' not in msg.keys():
            return False
    elif msg['type'] == 'info':
        if 'infoStr' not in msg.keys():
            return False
    elif msg['type'] == 'err':
        if 'errStr' not in msg.keys():
            return False
    else:
        #如果出现没有规定的type，也不合法
        return False

    #以上条件皆满足，则为正确的消息
    return True

if __name__ == '__main__':
    res = loadJson('')
    res = dumpJson(res)
    print(res)
    print(type(res))