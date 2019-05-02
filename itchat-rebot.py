import itchat
import requests
from itchat.content import *
import time
import json

#login
itchat.auto_login(hotReload=True, enableCmdQR=2)


key = '8b8b0e3722b14680bd750a6a9311235f'
apiUrl = 'http://www.tuling123.com/openapi/api'
group_punch = []
last_dateDay = None
now_dateDay = None

#图灵
def rebot(msg, userid='rebot'):
    data = {
        "key": key,
        "info": msg,
        "userid": userid
    }

    r = requests.post(apiUrl, data=data).json()

    return r['text']

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    reply = rebot(msg.text)
    msg.user.send(reply)

#成功打卡成员
def success_punch(group):

    member = time.strftime("%B %d", time.localtime()) + '打卡记录 \n'
    for item in group:
        if group.index(item) != (len(group) - 1):
            member += str(group.index(item) + 1) + '.' + item + '\n'
        else:
            member += str(group.index(item) + 1) + '.' + item

    return member

#json
def data(group):
    data = {}
    try:
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
            f.close()
    except FileNotFoundError:
        with open('data.json', "w") as f:
            f.write(json.dumps(data))
            f.close()
    date = str(time.localtime().tm_mon) + str(time.localtime().tm_mday)
    data[date] = group
    print(data)

    with open('data.json', 'w') as f:
        f.write(json.dumps(data))
        f.close()


# 打卡
@itchat.msg_register(TEXT, isGroupChat=True)
def group_reply(msg):
    global last_dateDay
    global now_dateDay
    global group_punch

    if last_dateDay == None and now_dateDay == None:
        last_dateDay = now_dateDay = time.localtime(time.time()).tm_mday
    else:
        now_dateDay = time.localtime(time.time()).tm_mday


    if now_dateDay != last_dateDay:
        data(group_punch)
        group_punch = []
        last_dateDay = now_dateDay


    print(last_dateDay)

    if msg.isAt:
        # print(msg)
        if msg.text.find("打卡") != -1:
            if msg.actualNickName in group_punch:
                msg.user.send('@' + msg.actualNickName + ' 你已经打卡了，不需要重复打卡')
            else:
                msg.user.send('打卡成功')
                group_punch.append(msg.actualNickName)

            msg.user.send(success_punch(group_punch))
        else:
            reply = rebot(msg.text, userid=msg.MsgId)
            msg.user.send(reply)

itchat.run(True)
