'''
学习使用select模块
参考链接：https://www.jianshu.com/p/e26594304e11
参考他的代码重新写了一遍
'''
import select
import socket

# 初始化服务端socket
serSock = socket.socket()
serSock.bind(('127.0.0.1', 12346))
serSock.listen(5)

readList = [serSock]
writeList = []
message_dict = {}#存储消息用的字典，键为socket，值为消息列表
i=0
while True:
    print('循环数：'+str(i))
    i+=1
    # select函数阻塞timeout时间，从参数的三个列表中，选择出此时可读取、可写入、出现错误的元素返回
    readableList, writableList, exceptionList = select.select(readList, writeList, readList, 1)

    for sock in readableList:
        # 遍历当前可读取的socket
        if sock is serSock:
            # 如果是服务端socket，那么就是有客户端来连接了
            cliSock, cliAddr = sock.accept()
            readList.append(cliSock)  # 将新的客户端socket加入监听列表
            message_dict[cliSock] = []#为新的socket创建消息列表
        else:
            # 已连接的用户发送消息过来
            # 接收一下
            data = sock.recv(1024)
            if not data:
                # 如果收到空数据，代表客户端已经断开连接
                readList.remove(sock)
                del message_dict[sock]#删除对应的消息队列
                print('一个客户端断开了连接')
                sock.close()

            else:
                #收到老用户的消息
                dataStr = data.decode()
                #将消息加入对应的消息队列
                message_dict[sock].append(dataStr)
                writeList.append(sock)
    
    for sock in writableList:
        # 处理消息队列中的消息
        while len(message_dict[sock]) > 0:
            dataStr = message_dict[sock][0]#取出消息队列中第一个消息
            del message_dict[sock][0]
            sock.sendall(('echo:'+dataStr).encode())
        #将消息队列中所有消息处理完毕，则将它从待回复队列中删除
        writeList.remove(sock)

    for sock in exceptionList:
        readList.remove(sock)