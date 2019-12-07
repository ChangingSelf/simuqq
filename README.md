# simuqq
 仿qq即时通信软件



## 功能需求

- 用账号密码登录
- 通过账号添加好友
- 查看好友是否在线
- 与好友聊天



### 账号密码登录

客户端利用登录对话框获取账号密码，与数据文件中已注册的账号密码对比
- 如果不匹配，登录失败
- 如果匹配，登录成功，打开主界面

### 通过账号添加好友

客户端获取账号后，查找数据文件
- 如果不存在，则添加失败
- 如果存在该账号，则将该账号添加到本账号好友列表

### 显示好友列表

主页面读取数据文件来显示好友列表，询问服务端每个好友是否在线

### 与在线好友聊天

打开在线好友的聊天框，发送与接收聊天信息



## 一些问题

### 服务端和客户端通信方式

双方发送的都是json字符串，解析出来是一个字典，不是所有的字段都被设置：

```python
{
    'userName':用户名,
    'password':密码,
    'errStr':错误字符串,
    'infoStr':信息字符串,
    'message':聊天消息
}
```

