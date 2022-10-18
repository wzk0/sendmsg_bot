# 一个Telegram机器人!

## 有什么功能呢?

1. 允许设置主人列表
2. 支持注册签到
3. 支持主人增加用户积分
4. 支持推送消息到注册用户(可设置条件)
5. 本地数据保存
6. 支持日志记录

## 如何使用呢?

![如图所示](https://ghproxy.com/https://raw.githubusercontent.com/wzk0/photo/main/202210182316712.png)
只需在图片中的位置编辑参数即可,
使用bot可向bot发送/help指令.

## 工作流程呢?

通过写入.temp文件判断更新,通过写入.offset文件获取更新,通过创建.data文件夹保留用户id信息,id为子文件夹,内有last_time(最近的更新时间)和point(积分),都是明文储存.
![结构](https://ghproxy.com/https://raw.githubusercontent.com/wzk0/photo/main/202210182319431.png)

## 开发相关呢?

关键处在于235行的`command()`函数(位于108行),只需编辑此函数即可完成对新功能的封装.

对于非文本消息的处理例子:
**怎么了,给我发这个photo,想和我聊天嘛?**

对于非指令的文本消息的处理:
使用[青云客智能聊天机器人API](http://api.qingyunke.com).
